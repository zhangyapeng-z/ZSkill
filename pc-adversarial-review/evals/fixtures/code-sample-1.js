// 用户登录接口 - Node.js + Express + MySQL
// 测试用例：包含 SQL 注入、无输入校验、错误处理缺失等问题

const express = require('express');
const mysql = require('mysql');
const app = express();

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password123',
  database: 'mydb'
});

app.post('/login', (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  // SQL 查询：直接拼接用户输入
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

  db.query(query, (err, result) => {
    if (result.length > 0) {
      // 登录成功，返回用户信息和 token
      res.json({
        success: true,
        user: result[0],
        token: 'fake-jwt-token-' + result[0].id
      });
    } else {
      // 登录失败
      res.json({ success: false });
    }
  });
});

// 获取用户信息
app.get('/user/:id', (req, res) => {
  const userId = req.params.id;
  const query = `SELECT * FROM users WHERE id = ${userId}`;

  db.query(query, (err, result) => {
    res.json(result[0]);
  });
});

// 修改密码
app.post('/change-password', (req, res) => {
  const userId = req.body.userId;
  const newPassword = req.body.newPassword;

  const query = `UPDATE users SET password = '${newPassword}' WHERE id = ${userId}`;
  db.query(query, (err, result) => {
    res.json({ success: true });
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});

// 测试用例说明：
// P0 问题：
// 1. SQL 注入漏洞（所有数据库查询都直接拼接用户输入）
// 2. 数据库密码硬编码在代码中
// 3. 明文存储密码
// 4. /change-password 接口无鉴权（任何人都能改别人密码）
//
// P1 问题：
// 1. 无输入校验（用户名、密码格式不验证）
// 2. 错误处理缺失（db.query 的 err 完全没处理）
// 3. token 是假的，没有真正的 JWT 认证
// 4. /user/:id 接口可能返回敏感信息
//
// P2 问题：
// 1. 代码重复（每个路由都手写 SQL 查询）
// 2. 没有连接池
// 3. 没有日志
