# Tech Stack Detection Rules

This file documents how the scan_project.py script detects the technology stack from project files.

---

## Detection Sources

The script uses three primary sources for tech stack detection:

1. **POM dependencies** (`pom.xml`) — Maven dependency `groupId:artifactId` strings
2. **Gradle dependencies** (`build.gradle`) — implementation/testImplementation declarations
3. **Config files** (`application.yml`, `application.properties`) — connection strings and property keys
4. **Source code** — annotation patterns (`@FeignClient`, `@RestController`, etc.)
5. **File presence** — `Dockerfile`, `Chart.yaml`, `docker-compose.yml`, etc.

---

## Technology Detection Rules

### Web Frameworks

| Technology | Detection Method |
|-----------|-----------------|
| Spring Boot | POM contains `spring-boot-starter` or `spring-boot-dependencies`; OR config file `application.yml` exists |
| Spring Cloud | POM contains `spring-cloud-starter` or `spring-cloud-dependencies` |
| Spring Cloud Alibaba | POM contains `spring-cloud-alibaba`, `nacos`, `sentinel`, `seata`, or `dubbo` |
| Spring Security | POM contains `spring-security` or `spring-boot-starter-security` |

### Data Access

| Technology | Detection Method |
|-----------|-----------------|
| MyBatis | POM contains `mybatis`, `mybatis-spring`, or `mybatis-spring-boot-starter`; OR mapper XML files exist |
| MyBatis-Plus | POM contains `mybatis-plus` or `mybatis-plus-boot-starter` |
| JPA/Hibernate | POM contains `hibernate-core`, `spring-data-jpa`, or `jpa` |
| ShardingSphere | POM contains `shardingsphere` or `sharding-jdbc` |

### Databases

| Technology | Detection Method |
|-----------|-----------------|
| MySQL | Config contains `jdbc:mysql://`; OR POM contains `mysql-connector-java` |
| PostgreSQL | Config contains `jdbc:postgresql://`; OR POM contains `postgresql` |
| Oracle | Config contains `jdbc:oracle:`; OR POM contains `ojdbc` |
| SQL Server | Config contains `jdbc:sqlserver:`; OR POM contains `mssql-jdbc` |
| MongoDB | Config contains `mongodb://`; OR POM contains `spring-boot-starter-data-mongodb` |

### Caching

| Technology | Detection Method |
|-----------|-----------------|
| Redis | Config contains `redis:` or `spring.redis`; OR POM contains `spring-boot-starter-data-redis`, `jedis`, `lettuce`, `redisson` |

### Message Queues

| Technology | Detection Method |
|-----------|-----------------|
| Kafka | Config contains `spring.kafka` or `bootstrap-servers`; OR POM contains `spring-kafka`, `kafka-clients` |
| RabbitMQ | Config contains `spring.rabbitmq` or `amqp`; OR POM contains `spring-boot-starter-amqp`, `amqp-client` |
| RocketMQ | Config contains `rocketmq`; OR POM contains `rocketmq-spring-boot-starter`, `rocketmq-client` |

### Search Engines

| Technology | Detection Method |
|-----------|-----------------|
| Elasticsearch | Config contains `spring.elasticsearch`; OR POM contains `spring-data-elasticsearch`, `elasticsearch-rest-high-level-client` |

### Service Registry / Discovery

| Technology | Detection Method |
|-----------|-----------------|
| Nacos | Config contains `spring.cloud.nacos`; OR POM contains `spring-cloud-starter-alibaba-nacos`, `nacos-client` |
| Zookeeper | Config contains `zookeeper` or `curator`; OR POM contains `zookeeper`, `curator` |

### Service Communication

| Technology | Detection Method |
|-----------|-----------------|
| Feign | POM contains `spring-cloud-starter-openfeign` or `feign`; OR source code contains `@FeignClient` |
| gRPC | POM contains `grpc` or `grpc-spring-boot-starter` |
| Dubbo | POM contains `dubbo-spring-boot-starter` or `dubbo` |

### Distributed Infrastructure

| Technology | Detection Method |
|-----------|-----------------|
| Seata (distributed transaction) | Config/POM contains `seata` or `spring.cloud.alibaba.seata` |
| Sentinel (flow control) | Config/POM contains `sentinel` or `spring.cloud.sentinel` |
| MinIO (object storage) | Config/POM contains `minio` |

### Utility Libraries

| Technology | Detection Method |
|-----------|-----------------|
| Lombok | POM contains `lombok` |
| MapStruct | POM contains `mapstruct` |
| Hutool | POM contains `hutool` |
| JWT | POM contains `jjwt`, `java-jwt`, or `auth0` |

### API Documentation

| Technology | Detection Method |
|-----------|-----------------|
| Swagger/OpenAPI | POM contains `springfox`, `springdoc`, or `swagger` |

### Deployment Infrastructure

| Technology | Detection Method |
|-----------|-----------------|
| Docker | `Dockerfile` or `docker-compose.yml` exists in project |
| Kubernetes | Files in `k8s/` directory, or `deployment.yaml`, `service.yaml`, `ingress.yaml` exist |
| Helm Chart | `Chart.yaml` exists; OR `charts/` directory with `Chart.yaml` |

---

## Version Extraction

Where possible, the scanner extracts version information:

1. **Explicit version in POM `<dependency>`**: `<version>2.7.0</version>`
2. **Property reference in POM**: `<version>${spring-boot.version}</version>` → resolve from `<properties>`
3. **Parent POM managed versions**: Inherited from parent POM
4. **Gradle version string**: `implementation 'org.springframework.boot:spring-boot-starter:3.1.0'`

---

## Build Tool Detection

| Build Tool | Detection Method |
|-----------|-----------------|
| Maven | `pom.xml` exists in project root |
| Gradle (Groovy) | `build.gradle` exists in project root |
| Gradle (Kotlin) | `build.gradle.kts` exists in project root |

---

## Module Detection

### Maven Multi-Module
- Parse root `pom.xml` `<modules>` section
- Each `<module>` element gives a module directory name
- Parse each module's `pom.xml` for `artifactId`, `packaging`, `dependencies`

### Gradle Multi-Project
- Parse `settings.gradle` for `include` statements
- Each `include 'module-name'` gives a subproject
- Parse each subproject's `build.gradle` for dependencies

---

## Layer Detection (DDD Architecture)

The scanner identifies DDD layers by matching package name patterns:

| Layer | Package Patterns |
|-------|-----------------|
| Controller | `.controller`, `.api`, `.web`, `.interfaces` |
| Service | `.service`, `.application`, `.app.service` |
| Domain | `.domain`, `.model`, `.entity`, `.vo` |
| Repository | `.repository`, `.mapper`, `.infrastructure`, `.infra`, `.dao` |
| DTO | `.api.dto`, `.dto`, `.vo`, `.request`, `.response` |
| Config | `.config`, `.configuration` |

---

## Key Annotation Detection

The scanner counts occurrences of these Spring annotations to provide a code structure summary:

| Annotation | Meaning |
|-----------|---------|
| `@RestController` / `@Controller` | API entry points |
| `@Service` | Service layer classes |
| `@Repository` / `@Mapper` | Data access layer |
| `@Configuration` | Configuration classes |
| `@FeignClient` | Inter-service call clients |
| `@Component` | Spring components |
| `@Entity` / `@TableName` / `@Table` | Domain entities |
| `@RestControllerAdvice` | Global exception handlers |
| `@Scheduled` | Scheduled tasks |
