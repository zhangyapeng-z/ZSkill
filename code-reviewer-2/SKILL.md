---
name: "code-reviewer"
description: "Reviews code for best practices, bugs, and improvements. Invoke when user asks for code review or before merging changes."
---

# Code Reviewer

This skill reviews code and provides feedback on:

1. **Best Practices**: Ensures code follows Java Alibaba development guidelines and industry standards
2. **Bugs**: Identifies potential issues and vulnerabilities
3. **Performance**: Suggests optimizations for better execution efficiency
4. **Maintainability**: Improves code readability and structure
5. **Security**: Checks for potential security vulnerabilities

## Usage Guidelines

### When to Invoke
- User explicitly asks for code review
- Before merging changes to ensure code quality
- When refactoring existing code
- When implementing new features that require quality assurance

### How to Use
1. Specify the file or code snippet to review
2. Mention any specific aspects to focus on (e.g., performance, security)
3. The skill will analyze the code and provide detailed feedback

## Review Process

1. **Code Analysis**: Examines the code structure, syntax, and logic
2. **Issue Identification**: Detects potential problems and areas for improvement
3. **Feedback Generation**: Provides specific, actionable recommendations
4. **Best Practice Enforcement**: Ensures compliance with Java Alibaba development guidelines

## Example

To review a file:

```
请帮我 review 一下 CostCalServiceImpl.java 文件，重点关注性能优化和代码结构。
```

The skill will then analyze the file and provide detailed feedback on performance bottlenecks, code structure improvements, and adherence to best practices.