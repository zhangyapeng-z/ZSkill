# 阿里巴巴 Java 开发手册检查规则

本文档基于《阿里巴巴Java开发手册（华山版）》定义代码质量检查规则，覆盖命名规范、注释规范、异常处理、日志规范、集合处理、并发处理、控制语句、OOP 规范八大类。

---

## 一、命名规范 [C-01]

### 1.1 类命名规则

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| N-01 | 类名使用 UpperCamelCase（大驼峰） | Major | 正则：`^[A-Z][a-zA-Z0-9]*$` |
| N-02 | 抽象类以 `Abstract` 或 `Base` 开头 | Major | 检查 `abstract class` 名称前缀 |
| N-03 | 异常类以 `Exception` 结尾 | Major | 检查继承 `Exception/RuntimeException` 的类名后缀 |
| N-04 | 测试类以 `Test` 结尾 | Minor | 检查 `src/test/java/` 下的类名后缀 |
| N-05 | 枚举类以 `Enum` 结尾或使用复数形式 | Minor | 检查 `enum` 声明的类名 |

### 1.2 方法与变量命名规则

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| N-06 | 方法名/变量名使用 lowerCamelCase（小驼峰） | Major | 正则排除全小写/下划线分隔的变量名 |
| N-07 | 常量名全大写，下划线分隔 | Major | 检查 `static final` 字段命名 |
| N-08 | 包名全小写，点分隔 | Major | 检查 `package` 声明 |
| N-09 | boolean 变量名不以 `is` 开头（避免序列化问题） | Major | 检查 boolean 类型字段名前缀 |

### 1.3 检查伪代码

```python
def check_naming(java_file):
    issues = []
    for class_def in parse_classes(java_file):
        # N-01: 类名 UpperCamelCase
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', class_def.name):
            issues.append(rule("N-01", "Major", class_def.line, 
                f"类名 {class_def.name} 不符合 UpperCamelCase 规范"))
        
        # N-02: 抽象类前缀
        if class_def.is_abstract and not re.match(r'^(Abstract|Base)', class_def.name):
            issues.append(rule("N-02", "Major", class_def.line,
                f"抽象类 {class_def.name} 应以 Abstract 或 Base 开头"))
        
        # N-03: 异常类后缀
        if class_def.extends_exception and not class_def.name.endswith('Exception'):
            issues.append(rule("N-03", "Major", class_def.line,
                f"异常类 {class_def.name} 应以 Exception 结尾"))
        
        # N-09: boolean 字段不以 is 开头
        for field in class_def.fields:
            if field.type == 'boolean' and field.name.startswith('is'):
                issues.append(rule("N-09", "Major", field.line,
                    f"boolean 变量 {field.name} 不应以 is 开头"))
    
    return issues
```

---

## 二、注释规范 [C-02]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| CM-01 | 类必须有 Javadoc 注释，包含作者和功能说明 | Minor | 检查类声明上方是否有 `/** */` |
| CM-02 | 公有方法必须有 Javadoc 注释 | Minor | 检查 `public` 方法上方是否有 `/** */` |
| CM-03 | 公有字段必须有 Javadoc 注释 | Minor | 检查 `public` 字段上方是否有 `/** */` |
| CM-04 | 废弃方法必须标注 `@Deprecated` | Major | 检查注释中是否有"已废弃"/"deprecated"但无注解 |
| CM-05 | TODO/FIXME 注释必须标注负责人和预计完成时间 | Minor | 检查 TODO/FIXME 注释格式 |
| CM-06 | 注释使用中文，字符编码统一为 UTF-8 | Minor | 检查注释内容是否含中文 |

---

## 三、异常处理 [C-03]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| E-01 | 禁止捕获 `Exception` 或 `Throwable` 后不做任何处理 | Critical | 检查 `catch(Exception` 后 catch 块是否为空或仅注释 |
| E-02 | catch 块不能为空（仅注释也视为空） | Critical | 检查 `catch` 块体是否为空 |
| E-03 | 禁止在 finally 块中使用 `return`、`continue`、`break` | Critical | 检查 `finally` 块中是否有这些语句 |
| E-04 | 禁止用 `RuntimeException` 替代具体异常 | Major | 检查 `throw new RuntimeException` 的使用 |
| E-05 | 方法返回值可能为 null 时应标注 `@Nullable` | Major | 检查返回对象类型的方法是否有 null 判断调用方 |
| E-06 | 禁止 `try-catch` 中嵌套 `try-catch` 超过 3 层 | Major | 统计 try-catch 嵌套深度 |
| E-07 | 异常信息必须包含上下文信息（不能仅 `e.getMessage()`） | Minor | 检查 log.error 的参数 |
| E-08 | 自定义异常应继承 `RuntimeException` 而非 `Exception` | Minor | 检查自定义异常的父类 |

### 检查伪代码

```python
def check_exception_handling(java_file):
    issues = []
    lines = read_lines(java_file)
    
    for i, line in enumerate(lines):
        # E-01: catch(Exception e) {} 空处理
        if re.search(r'catch\s*\(\s*(Exception|Throwable)\s+\w+\s*\)', line):
            # 检查 catch 块体是否为空
            block_body = extract_block_body(lines, i)
            if is_empty_or_comment_only(block_body):
                issues.append(rule("E-01", "Critical", i+1,
                    "捕获 Exception/Throwable 后未做任何处理"))
            elif not has_logging(block_body) and not has_rethrow(block_body):
                issues.append(rule("E-01", "Critical", i+1,
                    "捕获 Exception/Throwable 后既未记录日志也未重新抛出"))
        
        # E-03: finally 中 return/continue/break
        if in_finally_block(lines, i):
            if re.search(r'\b(return|continue|break)\b', line):
                issues.append(rule("E-03", "Critical", i+1,
                    "finally 块中禁止使用 return/continue/break"))
    
    return issues
```

---

## 四、日志规范 [C-04]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| L-01 | 使用 SLF4J 门面（`LoggerFactory.getLogger`），禁止直接使用 Log4j/Logback | Major | 检查 import 是否为 `org.slf4j.Logger` |
| L-02 | 日志使用占位符 `{}`，禁止字符串拼接 | Major | 检查 `log.xxx()` 调用中是否使用 `+` 拼接 |
| L-03 | ERROR 日志必须记录异常堆栈（传入 Throwable 参数） | Critical | 检查 `log.error()` 是否有 Exception 参数 |
| L-04 | 禁止在循环体内打印日志 | Major | 检查 for/while 块内是否有 log 调用 |
| L-05 | DEBUG 级别日志前需判断 `log.isDebugEnabled()` | Major | 检查 `log.debug()` 前是否有级别判断 |
| L-06 | 禁止使用 `System.out.println` / `System.err.println` | Major | 搜索 `System.out` / `System.err` |
| L-07 | 禁止使用 `e.printStackTrace()` | Critical | 搜索 `printStackTrace` 调用 |
| L-08 | 日志内容使用中文或结构化英文，避免无意义内容 | Minor | 人工审查 |

---

## 五、集合处理 [C-05]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| CL-01 | 禁止在 foreach 循环中对集合执行 `remove`/`add` | Critical | 检查 `for(:)` 内是否有 `add/remove` |
| CL-02 | 使用 `isEmpty()` 判断空集合，禁止 `size() == 0` | Major | 正则搜索 `\.size\(\)\s*==\s*0` |
| CL-03 | 集合转 Map 时注意 key 冲突（`Collectors.toMap` 需指定 mergeFunction） | Critical | 检查 `toMap` 是否有第三个参数 |
| CL-04 | 返回集合时使用 `Collections.unmodifiableXxx` 或 Guava `ImmutableList` | Major | 检查 public 方法返回 `List/Set/Map` 是否包装为只读 |
| CL-05 | 多线程环境使用 `ConcurrentHashMap` 而非 `HashMap` | Critical | 检查并发上下文中是否使用非线程安全集合 |
| CL-06 | 集合初始化时指定容量（`new ArrayList<>(expectedSize)`） | Minor | 检查 `new ArrayList<>()` 无参构造 |
| CL-07 | 禁止使用 `SubList` 返回给外部使用（可能导致 ConcurrentModificationException） | Major | 检查方法返回值是否为 `subList()` 结果 |

---

## 六、并发处理 [C-06]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| CC-01 | 禁止使用 `new Thread()` 创建线程，必须使用线程池 | Critical | 搜索 `new Thread(` |
| CC-02 | 线程池必须通过 `ThreadPoolExecutor` 创建，禁止使用 `Executors` 工具类 | Critical | 检查 `Executors.newXxx` 调用 |
| CC-03 | `SimpleDateFormat` 线程不安全，禁止作为静态变量或共享变量 | Critical | 检查 `static.*SimpleDateFormat` |
| CC-04 | 对共享可变变量使用 `volatile` 或 `Atomic` 类 | Major | 检查多线程访问的可变变量 |
| CC-05 | 禁止锁嵌套（`synchronized` 嵌套 `synchronized`） | Critical | 检查 synchronized 块嵌套 |
| CC-06 | `synchronized` 应使用最小粒度，避免锁定整个方法（除非必要） | Minor | 检查 `synchronized` 修饰方法 |
| CC-07 | 创建线程池需指定合理的队列容量和拒绝策略 | Major | 检查 `ThreadPoolExecutor` 构造参数 |
| CC-08 | 禁止使用 `Thread.stop()`、`Thread.suspend()`、`Thread.resume()` | Critical | 搜索这些方法调用 |

---

## 七、控制语句 [C-07]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| CS-01 | `if`/`else`/`for`/`while`/`do` 必须使用大括号 `{}`，即使只有一行 | Major | 检查控制语句后是否有 `{` |
| CS-02 | 禁止魔法值（代码中直接出现的未解释的字面量） | Major | 检查代码中的数字/字符串字面量 |
| CS-03 | `switch` 语句必须包含 `default` 分支 | Major | 检查 switch 是否有 default |
| CS-04 | 三目运算符注意自动拆箱导致的空指针 | Critical | 检查三目表达式中是否有包装类型 |
| CS-05 | 禁止在条件表达式中使用赋值语句（`if (a = b)`） | Major | 检查 if 条件中是否有 `=` 赋值 |
| CS-06 | `for` 循环中避免在大循环中做数据库查询或 RPC 调用 | Major | 人工审查 for 循环体内的远程调用 |

### 魔法值检测

```python
def check_magic_values(java_file):
    issues = []
    # 允许的常量：0, 1, -1, "", true, false 等
    allowed = {0, 1, -1, 2}
    
    for i, line in enumerate(read_lines(java_file)):
        # 跳过注释和注解行
        if is_comment(line) or is_annotation(line):
            continue
        
        # 检查数字魔法值
        numbers = re.findall(r'\b(\d+)\b', line)
        for num in numbers:
            if int(num) not in allowed:
                # 检查是否在常量定义中
                if not re.search(r'(static\s+final|final\s+static)', line):
                    issues.append(rule("CS-02", "Major", i+1,
                        f"魔法值 {num}，建议定义为常量"))
    
    return issues
```

---

## 八、OOP 规范 [C-08]

| 规则编号 | 规则描述 | 严重级别 | 检查方式 |
|----------|----------|----------|----------|
| O-01 | 禁止使用 `@Deprecated` 标注的方法 | Major | 检查方法调用是否标注了 `@Deprecated` |
| O-02 | `equals` 方法应使用常量或确定非 null 的对象调用 | Critical | 检查 `xxx.equals()` 调用方是否可能为 null |
| O-03 | 所有 POJO 类必须重写 `toString()` | Minor | 检查 POJO 类（有 getter/setter）是否有 `toString` |
| O-04 | 构造方法中禁止写入业务逻辑 | Major | 检查构造方法体是否有非赋值语句 |
| O-05 | 序列化类新增字段需更新 `serialVersionUID` | Minor | 检查 `Serializable` 类是否有 `serialVersionUID` |
| O-06 | 禁止使用过时的类或方法 | Major | 检查 import 是否引用了标记废弃的 API |
| O-07 | 使用 `BigDecimal` 进行金额计算，禁止使用 `double`/`float` | Critical | 检查金额相关字段类型 |
| O-08 | `POJO` 类属性使用包装类型（`Integer` 而非 `int`），局部变量使用基本类型 | Minor | 检查 POJO 字段类型 |

### equals 空指针检测

```python
def check_equals_null_safety(java_file):
    issues = []
    lines = read_lines(java_file)
    
    for i, line in enumerate(lines):
        # 匹配 variable.equals("xxx") 模式
        matches = re.finditer(r'(\w+)\.equals\(', line)
        for match in matches:
            var_name = match.group(1)
            # 如果调用方不是字面量/常量/null，则可能有空指针风险
            if var_name not in ('this', 'super') and not var_name.isupper():
                # 检查是否有前置 null 判断
                if not has_null_check_before(lines, i, var_name):
                    issues.append(rule("O-02", "Critical", i+1,
                        f"equals 调用方 {var_name} 可能为 null，"
                        f"建议使用 Objects.equals() 或常量.equals(变量)"))
    
    return issues
```

---

## 九、规则汇总表

| 类别 | 规则数 | Blocker | Critical | Major | Minor |
|------|--------|---------|----------|-------|-------|
| 命名规范 (C-01) | 9 | 0 | 0 | 7 | 2 |
| 注释规范 (C-02) | 6 | 0 | 0 | 1 | 5 |
| 异常处理 (C-03) | 8 | 0 | 3 | 3 | 2 |
| 日志规范 (C-04) | 8 | 0 | 2 | 5 | 1 |
| 集合处理 (C-05) | 7 | 0 | 3 | 3 | 1 |
| 并发处理 (C-06) | 8 | 0 | 5 | 2 | 1 |
| 控制语句 (C-07) | 6 | 0 | 1 | 4 | 1 |
| OOP 规范 (C-08) | 8 | 0 | 2 | 3 | 3 |
| **合计** | **60** | **0** | **16** | **28** | **16** |
