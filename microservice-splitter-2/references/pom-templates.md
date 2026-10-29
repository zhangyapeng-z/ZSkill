# Maven 多模块 POM 模板

## 根 POM（parent）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 父 POM 坐标 -->
    <groupId>com.example</groupId>
    <artifactId>project-parent</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>  <!-- 关键：多模块父 POM 必须为 pom -->

    <name>Project Parent</name>
    <description>Multi-module project parent POM</description>

    <!-- 子模块声明 -->
    <modules>
        <module>common</module>
        <module>user</module>
        <module>order</module>
        <module>payment</module>
        <module>app</module>
    </modules>

    <!-- 统一版本管理 -->
    <properties>
        <java.version>17</java.version>
        <spring-boot.version>3.2.0</spring-boot.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- 依赖版本统一管理（不引入，仅声明版本） -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>

            <!-- 内部模块版本 -->
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>common</artifactId>
                <version>${project.version}</version>
            </dependency>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>user</artifactId>
                <version>${project.version}</version>
            </dependency>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>order</artifactId>
                <version>${project.version}</version>
            </dependency>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>payment</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- 所有模块共享的依赖（可选） -->
    <dependencies>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <version>${spring-boot.version}</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

---

## common 模块 POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>project-parent</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>common</artifactId>
    <packaging>jar</packaging>

    <name>Common Module</name>
    <description>共享 DTO、工具类、常量、异常定义</description>

    <dependencies>
        <!-- 仅声明第三方依赖，不依赖任何业务模块 -->
        <!-- 例如：validation, jackson, commons-lang3 等 -->

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-annotations</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

## 业务模块 POM（以 order 为例）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>project-parent</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>order</artifactId>
    <packaging>jar</packaging>

    <name>Order Module</name>
    <description>订单业务模块：CRUD、状态流转、查询</description>

    <dependencies>
        <!-- common -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>common</artifactId>
        </dependency>

        <!-- 依赖的其他业务模块 -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>user</artifactId>
        </dependency>

        <!-- 第三方依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

## app 启动模块 POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>project-parent</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>app</artifactId>
    <packaging>jar</packaging>

    <name>Application Module</name>
    <description>Spring Boot 启动模块，统一入口</description>

    <dependencies>
        <!-- 依赖所有业务模块（通过类路径加载） -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>common</artifactId>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>user</artifactId>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>order</artifactId>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>payment</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- 仅 app 模块需要 spring-boot-maven-plugin -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <!-- 确保最终 jar 包含所有模块 -->
                    <requiresUnpack>
                        <dependency>
                            <groupId>com.example</groupId>
                            <artifactId>common</artifactId>
                        </dependency>
                    </requiresUnpack>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

---

## Spring Boot 启动类模板

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 统一启动类 —— 通过类路径加载所有模块。
 *
 * scanBasePackages 使用 com.example 前缀，确保能扫描到所有子模块的
 * @Component, @Service, @Repository, @Controller 等注解。
 */
@SpringBootApplication(scanBasePackages = "com.example")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 关键配置项

```yaml
# application.yml (app 模块)

spring:
  application:
    name: project-name
  # 如果使用 JPA，确保实体类能被扫描到
  jpa:
    packages-to-scan: com.example

# 如有需要，显式声明各模块配置类
# spring:
#   autoconfigure:
#     exclude: ...
```

---

## Gradle 等价配置

如果使用 Gradle，对应的 `settings.gradle` 和 `build.gradle` 结构：

### settings.gradle

```groovy
rootProject.name = 'project-parent'

include 'common'
include 'user'
include 'order'
include 'payment'
include 'app'
```

### 根 build.gradle

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0' apply false
    id 'io.spring.dependency-management' version '1.1.4' apply false
}

subprojects {
    apply plugin: 'java'
    apply plugin: 'io.spring.dependency-management'

    group = 'com.example'
    version = '1.0.0'

    java {
        sourceCompatibility = '17'
    }

    repositories {
        mavenCentral()
    }

    dependencyManagement {
        imports {
            mavenBom "org.springframework.boot:spring-boot-dependencies:3.2.0"
        }
    }
}
```

### app/build.gradle

```groovy
plugins {
    id 'org.springframework.boot'
}

dependencies {
    implementation project(':common')
    implementation project(':user')
    implementation project(':order')
    implementation project(':payment')
}
```
