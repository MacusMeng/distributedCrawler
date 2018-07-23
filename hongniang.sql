/*
Navicat MySQL Data Transfer

Source Server         : 123.206.30.117
Source Server Version : 50721
Source Host           : 123.206.30.117:3306
Source Database       : pythonspider

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-04-24 21:40:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hongniang
-- ----------------------------
DROP TABLE IF EXISTS `hongniang`;
CREATE TABLE `hongniang` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `nickname` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户名称',
  `loveid` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户id',
  `photos` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的照片',
  `age` varchar(32) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户年龄',
  `height` varchar(32) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的身高',
  `ismarried` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户是否已婚',
  `yearincome` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户年收入',
  `education` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的学历',
  `workaddress` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的地址',
  `soliloquy` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的内心独白',
  `gender` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户的性别',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3956 DEFAULT CHARSET=latin1;
