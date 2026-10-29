# 代码质量检查规则

本文件定义代码质量维度的全部检查规则（Q-01 ~ Q-07），每条规则包含：判定目标、命中条件、排除条件（避免误报）、严重级别、解决方案与最佳实践。

---

## Q-01 代码规范

**判定目标**：遵循阿里巴巴 Java 开发手册核心条款。

**命中条件（命名规范 Major）**：
- 类名非 UpperCamelCase（`class orderService`）
- 方法/变量非 lowerCamelCase（`void GetOrder()`）
- 常量非全大写下划线（`final int maxCount = 10`）
- 抽象类未以 `Abstract`/`Base` 开头；异常类未以 `Exception` 结尾；测试类未以 `Test` 结尾

**命中条件（异常处理 Critical）**：
- `catch (Exception e) {}` 空块或仅 `e.printStackTrace()` 不处理
- `finally` 块中 `return`/`continue`/`break`
- 吞异常：catch 后既不抛出也不记录日志也不返回错误

**命中条件（日志规范 Major）**：
- 未用 SLF4J 门面（`System.out.println`、`new Logger()` 非 slf4j）
- 日志字符串拼接而非占位符 `{}`
- ERROR 日志未记录异常堆栈（`log.error("xxx")` 无异常参数）
- 循环内打印日志

**排除条件**：
- 测试代码、main 方法中的 `System.out` → 不报
- 第三方生成的代码（标注 `@Generated`）→ 不报

**严重级别**：Major（异常处理升 Critical）

**解决方案与最佳实践**：
1. 引入 checkstyle/spotbugs + 阿里巴巴 p3c 插件到构建流程，CI 强制阻断
2. 统一异常处理：全局 `@RestControllerAdvice` + 自定义业务异常，禁止吞异常
3. 日志统一 SLF4J + 占位符，ERROR 必带异常对象 `log.error("msg", e)`

---

## Q-02 安全漏洞

**判定目标**：识别常见安全漏洞与不安全实践。

**命中条件（SQL 注入 Blocker）**：
- MyBatis XML 中使用 `${}` 拼接用户输入（而非 `#{}`）
- JDBC `Statement` 拼接 SQL（`"select * from t where id=" + id`）
- JPA `@Query` 使用拼接而非参数绑定

**命中条件（硬编码密钥 Blocker）**：
- 源码硬编码数据库密码、API Key、Token、私钥（正则匹配 `password="..."`、`secret="..."`、`AKIA[0-9A-Z]{16}`、长 hex/base64 私钥串）

**命中条件（不安全反序列化 Blocker）**：
- 使用 `ObjectInputStream.readObject()` 反序列化外部输入
- Fastjson `parseObject` 未启用 AutoType 安全限制
- 使用已知有 RCE 漏洞的依赖版本（Fastjson < 1.2.83、Log4j < 2.17.1）

**命中条件（XSS Critical）**：
- 接口直接返回未转义的用户输入到前端渲染

**命中条件（SSRF Critical）**：
- 接口接收 URL 参数并直接发起 HTTP 请求（`restTemplate.getForObject(userUrl)`）

**命中条件（越权 Major）**：
- 查询/修改接口仅按请求参数 id 操作，未校验当前用户对该资源的归属权限

**排除条件**：
- `${}` 用于表名/列名等非用户可控字段（排序字段白名单校验过）→ 不报
- 硬编码为本地开发默认占位（`changeme`）且在 local profile → 提示不报 Blocker

**严重级别**：Blocker（SQL 注入/硬编码密钥/反序列化 RCE），Critical（XSS/SSRF），Major（越权）

**解决方案与最佳实践**：
1. SQL 一律参数化 `#{}`；动态表名/排序字段用白名单校验
2. 密钥走配置中心/环境变量/KMS，源码零明文
3. 反序列化用白名单；Fastjson 升级到 SafeMode；禁用 AutoType
4. 有漏洞依赖立即升级到安全版本（参见 Q-04）
5. SSRF：URL 校验协议与目标白名单，禁止访问内网地址
6. 越权：所有资源操作校验当前用户归属，用 `@PreAuthorize` 或业务层校验

---

## Q-03 性能瓶颈

**判定目标**：识别常见性能反模式。

**命中条件（N+1 查询 Critical）**：
- 循环内调用 Mapper/DAO/Feign 查询（`for (...) { mapper.selectById(id); }`）
- MyBatis 一对多关联未用 `fetchType=lazy` 或联合查询，导致主查询 N 次子查询

**命中条件（循环内 DB 调用 Critical）**：
- for/while/forEach 循环体内出现 `mapper.`/`dao.`/`jdbcTemplate.`/`feign` 调用

**命中条件（大结果集未分页 Critical）**：
- `selectList()`/`findAll()` 无 `limit`/`PageHelper` 且表为大表（结合表名行数估算或提示）

**命中条件（同步阻塞可异步 Major）**：
- 批量调用第三方/发邮件/发短信等 IO 密集操作同步串行（`for(url) restTemplate.post()`）

**命中条件（锁粒度过大 Critical）**：
- `synchronized` 锁整个方法且方法体含 IO/远程调用
- 锁 `this` 或大对象

**排除条件**：
- 循环内 DB 调用经核对为批量小数据且无性能问题 → 降级提示
- 同步调用经核对必须强一致串行 → 不报

**严重级别**：Critical（N+1/循环DB/大结果集/锁），Major（可异步化）

**解决方案与最佳实践**：
1. N+1：改批量查询 `selectByIds(List)` 一次取回，应用层组装
2. 循环 DB：提取为批量操作；MyBatis 用 `<foreach>` 批量
3. 大结果集：强制分页 `PageHelper.startPage`，接口禁绝全表返回
4. IO 密集批量：异步化（`@Async`/CompletableFuture/消息队列）
5. 锁：缩小临界区，只锁必要共享资源；IO 操作移出锁；用 `ReentrantLock.tryLock` 带超时

---

## Q-04 依赖管理

**判定目标**：识别依赖版本冲突与有漏洞的依赖。

**命中条件（版本冲突 Major）**：
- 同一 artifact 在依赖树存在多个版本（Maven `dependency:tree` 多版本）
- 直接依赖与传递依赖版本不一致，靠 `<exclusions>` 打补丁

**命中条件（已知 CVE 依赖 Blocker）**：
- 依赖版本命中已知漏洞库（内置常见 CVE 映射）：
  - `log4j-core` < 2.17.1（Log4Shell RCE）
  - `fastjson` < 1.2.83（AutoType RCE）
  - `spring-framework` < 5.3.20（CVE-2022-22965 Spring4Shell）
  - `shiro` < 1.7.1（认证绕过）
  - `jackson-databind` < 2.13.x（反序列化）

**命中条件（scope 滥用 Major）**：
- `compile` scope 引入 `test`/`provided` 性质依赖
- `spring-boot-starter-tomcat` 设为 `compile`（应 provided，容器提供）

**命中条件（SNAPSHOT 进生产 Major）**：
- 生产 profile 依赖含 `SNAPSHOT` 版本

**排除条件**：
- 版本冲突经核对为兼容（patch 版本差异无破坏性变更）→ 降级提示
- 漏洞版本经核对已通过其他方式缓解（如 WAF 拦截）→ 标记"待确认"

**严重级别**：Blocker（已知 CVE），Major（冲突/scope/SNAPSHOT）

**解决方案与最佳实践**：
1. 用 BOM 统一版本管理（`spring-boot-dependencies` BOM）
2. 已知 CVE 依赖立即升级到安全版本，CI 集成 OWASP Dependency-Check
3. scope 规范：测试依赖 `test`，容器提供 `provided`
4. 生产禁用 SNAPSHOT，发布前 Maven `enforcer` 插件强制校验

---

## Q-05 重复代码

**判定目标**：识别重复代码块与复制粘贴逻辑。

**命中条件**：
- 重复块：≥6 行且相似度 ≥80% 的代码块（基于 token 序列哈希比对）
- 重复的 DTO/Entity 转换逻辑（`toDTO`/`toEntity`/`convert` 方法雷同）
- 跨服务重复工具类（`DateUtils`/`StringUtils` 各服务各写一份）

**排除条件**：
- 重复为生成的代码（`@Generated`/mapstruct 生成）→ 不报
- 重复为接口契约不同实现（签名一致但语义不同）→ 不报
- 相似度 60%-80% → 标记"待确认"而非直接报

**严重级别**：Major

**解决方案与最佳实践**：
1. 公共逻辑抽取到 common-shared 模块或 starter 统一复用
2. DTO 转换用 MapStruct 生成，消除手写转换样板
3. 工具类统一沉淀到公共组件库，各服务依赖引用
4. 跨服务重复领域逻辑：评估是否应合并为同一服务或提取公共服务

---

## Q-06 并发处理

**判定目标**：识别线程不安全与并发反模式。

**命中条件**：
- `new Thread()` 直接创建线程（未用线程池）
- 线程池用 `Executors.newXxx()` 而非 `ThreadPoolExecutor`（无界队列 OOM 风险）
- `SimpleDateFormat` 作为静态/成员字段被多线程共享
- 共享可变状态无 `volatile`/`synchronized`/`Atomic` 保护
- 锁嵌套（多个锁嵌套获取，死锁风险）

**排除条件**：
- `new Thread()` 在测试代码中 → 不报
- `Executors.newSingleThreadExecutor` 经核对为单线程无并发 → 降级提示

**严重级别**：Critical

**解决方案与最佳实践**：
1. 一律用 `ThreadPoolExecutor`，明确核心/最大线程数、队列容量、拒绝策略
2. 线程池统一通过配置中心管理，禁止散落 new
3. `SimpleDateFormat` 用 `DateTimeFormatter`（线程安全）或 ThreadLocal
4. 共享状态用 `Atomic*`/`ConcurrentHashMap`/`volatile`
5. 锁按统一顺序获取，避免嵌套；用 `tryLock` 超时防死锁

---

## Q-07 资源管理

**判定目标**：识别资源泄漏与配置不合理。

**命中条件**：
- IO/连接/流未用 `try-with-resources`，`close` 在 finally 手写且可能漏关
- 连接池配置不合理：最大连接数过大（如 200）或过小、未配置最大等待时间
- 数据库连接/Redis 连接未配置池化（`new Connection()` 每次新建）

**排除条件**：
- 资源由框架自动管理（Spring 管理的连接）→ 不报

**严重级别**：Critical

**解决方案与最佳实践**：
1. IO/流一律 `try-with-resources` 自动关闭
2. 连接池参数按压测调优：HikariCP `maximumPoolSize` 按机器配置，`connectionTimeout` 设超时
3. 所有外部连接走连接池，禁止裸 new
4. Redis 连接池 Lettuce 默认即可，按需调 `max-active`/`max-wait`

---

## 误报排除总原则

1. **置信度分级**：脚本对每条疑似给置信度，high 自动计入，medium/low 标"待确认"
2. **技术栈感知**：非微服务工程不触发 M 系列微服务规则
3. **生成代码排除**：`@Generated`/mapstruct/lombok 生成代码不报规范类问题
4. **profile 感知**：`local`/`dev` profile 的宽松配置不报生产级问题
5. **人工复核**：语义级问题交人工确认后才计入正式报告
