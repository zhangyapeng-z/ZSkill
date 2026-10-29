# Spring Cloud / Dubbo 技术栈识别特征与检查映射

本文件定义主流微服务技术栈的识别特征（用于 `detect_tech_stack.py`）及其关联检查规则映射。

---

## 一、技术栈识别特征表

`detect_tech_stack.py` 的 `TECH_STACK_SIGNATURES` 配置，按以下特征匹配 POM 依赖与源码注解。

### Spring Cloud Netflix 体系

| 技术栈 | POM 依赖特征 | 源码特征 | 版本提示 |
|--------|-------------|----------|----------|
| Eureka Server | `spring-cloud-starter-netflix-eureka-server` | `@EnableEurekaServer` | 注册中心 |
| Eureka Client | `spring-cloud-starter-netflix-eureka-client` | `@EnableDiscoveryClient`/`@EnableEurekaClient` | 服务注册 |
| Hystrix 熔断 | `spring-cloud-starter-netflix-hystrix` | `@EnableCircuitBreaker`/`@HystrixCommand` | 熔断降级 |
| Zuul 网关 | `spring-cloud-starter-netflix-zuul` | `@EnableZuulProxy` | 网关（已废弃） |
| Ribbon 负载均衡 | `spring-cloud-starter-netflix-ribbon` | `@LoadBalanced` | 客户端负载均衡 |
| OpenFeign | `spring-cloud-starter-openfeign` | `@EnableFeignClients`/`@FeignClient` | 声明式 HTTP |

### Spring Cloud Alibaba 体系

| 技术栈 | POM 依赖特征 | 源码特征 | 版本提示 |
|--------|-------------|----------|----------|
| Nacos Discovery | `spring-cloud-starter-alibaba-nacos-discovery` | `@EnableDiscoveryClient` | 注册发现+配置 |
| Nacos Config | `spring-cloud-starter-alibaba-nacos-config` | `bootstrap.yml` 含 `nacos.config` | 配置中心 |
| Sentinel | `spring-cloud-starter-alibaba-sentinel` | `@SentinelResource` | 流控熔断 |
| Seata | `spring-cloud-starter-alibaba-seata` | `@GlobalTransactional` | 分布式事务 |
| RocketMQ | `spring-cloud-starter-stream-rocketmq`/`rocketmq-spring-boot-starter` | `@RocketMQMessageListener` | 消息最终一致 |

### Spring Cloud 通用

| 技术栈 | POM 依赖特征 | 源码特征 | 版本提示 |
|--------|-------------|----------|----------|
| Spring Cloud Gateway | `spring-cloud-starter-gateway` | `@EnableDiscoveryClient`+路由配置 | 网关 |
| Spring Cloud Config | `spring-cloud-config-server`/`spring-cloud-starter-config` | `@EnableConfigServer` | 配置中心 |
| Spring Cloud Sleuth | `spring-cloud-starter-sleuth` | 链路追踪 | — |
| Resilience4j | `resilience4j-spring-boot2` | `@CircuitBreaker`/`@Retry`/`@RateLimiter` | 新一代熔断 |

### Apache Dubbo 体系

| 技术栈 | POM 依赖特征 | 源码特征 | 版本提示 |
|--------|-------------|----------|----------|
| Dubbo（新） | `dubbo-spring-boot-starter`（3.x） | `@DubboService`/`@DubboReference` | Dubbo3 |
| Dubbo（旧） | `dubbo`/`dubbo-spring-boot-starter`（2.x） | `@Service`（dubbo）/`@Reference` | Dubbo2 |
| Dubbo 注册中心 | `dubbo.registry.address=zookeeper://...`/`nacos://...` | `application.dubbo.yml` | 注册发现 |

### 基础设施

| 技术栈 | POM 依赖特征 | 源码特征 | 版本提示 |
|--------|-------------|----------|----------|
| Spring Boot | `spring-boot-starter` | `@SpringBootApplication` | 基础框架 |
| MyBatis | `mybatis-spring-boot-starter` | `@Mapper`/`@MapperScan` | ORM |
| JPA/Hibernate | `spring-boot-starter-data-jpa` | `@Entity`/`@Repository` | ORM |
| Redis | `spring-boot-starter-data-redis` | `@RedissonClient`/`RedisTemplate` | 缓存 |
| Kafka | `spring-kafka` | `@KafkaListener` | 消息 |
| RabbitMQ | `spring-boot-starter-amqp` | `@RabbitListener` | 消息 |

---

## 二、检查规则映射表

按识别到的技术栈，决定触发哪些检查规则（避免对未使用的技术栈误报）。

| 技术栈 | 关联检查规则 | 说明 |
|--------|------------|------|
| OpenFeign 存在 | M-02 通信效率、M-04 分布式事务、M-05 熔断、M-09 幂等 | Feign 调用链相关 |
| Hystrix/Sentinel/Resilience4j 存在 | M-05 容错熔断（检查是否正确配置） | 有熔断框架则检查配置完整性 |
| 无任何熔断框架但存在跨服务调用 | M-05 容错熔断缺失（Critical） | 强报 |
| Spring Cloud Gateway/Zuul 存在 | M-06 网关配置 | 有网关则查网关配置 |
| Nacos/Eureka 存在 | M-07 注册发现（检查是否走注册中心） | 有注册中心则查硬编码 |
| Dubbo 存在 | M-02/M-05/M-09（按 Dubbo 特征检查） | RPC 调用链、mock/timeout、幂等 |
| Seata/RocketMQ 存在 | M-04 分布式事务（检查是否正确使用） | 有事务方案则检查覆盖完整性 |
| 无任何分布式事务方案但存在跨服务写 | M-04 分布式事务缺失（Critical） | 强报 |
| 多服务 datasource 指向同库 | M-03 共享库（Blocker） | 配置解析对比 |

---

## 三、判定优先级与排除

1. **先识别再检查**：技术栈识别为空（非微服务工程）→ 跳过全部 M 系列规则，仅执行 Q 系列代码质量检查
2. **框架版本感知**：Zuul 已废弃、Hystrix 停更，识别到时提示迁移到 Gateway/Resilience4j（提示而非报错）
3. **混合栈**：同时存在 Spring Cloud 与 Dubbo 时，两套规则都执行，分别按各自命中条件判断
4. **配置文件解析**：`application.yml`/`application.properties`/`bootstrap.yml`/`application-{profile}.yml` 均纳入解析，区分 profile

---

## 四、服务调用链识别规则

用于构建 `service-call-graph.json`：

| 调用方式 | 识别特征 | 调用方→被调方提取 |
|---------|----------|------------------|
| Feign | `@FeignClient(name="x")` 或 `@FeignClient(contextId="x")` | 当前服务 → name 指向的服务 |
| Dubbo | `@DubboReference`/`@Reference` 的 `interfaceClass` 包名 | 当前服务 → 接口归属服务 |
| RestTemplate | `restTemplate.getForObject("http://SERVICE-NAME/...")` | 当前服务 → SERVICE-NAME |
| WebClient | `webClient.get().uri("http://SERVICE-NAME/...")` | 当前服务 → SERVICE-NAME |
| 直接 URL | `http://192.168.x.x`/`http://host:port` | 标记为 M-07 硬编码 |

调用链深度计算：对调用图做 DFS 最长路径与环路检测。
