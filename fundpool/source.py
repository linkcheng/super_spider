#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import pymysql.cursors
from pymysql.cursors import DictCursor


def create_fund_pool():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '12345678',
        'db': 'fund_pool',
        'charset': 'utf8',
    }

    con = pymysql.connect(**config)
    cursor = con.cursor(DictCursor)

    domain = 'http://fund.eastmoney.com/'
    sql = 'insert into fund_pool.FundPool (`code`, `url`) values (%s, %s)'
    pool_depth = 1000000
    gradient = 100

    for i in range(gradient):
        tmp_pool = pool_depth / gradient
        params = [(str(tmp_pool*i+j).zfill(6), domain+str(tmp_pool*i+j).zfill(6)+'.html') for j in range(tmp_pool)]
        try:
            cursor.executemany(sql, params)
        except Exception as e:
            print(e)

        con.commit()

    cursor.close()
    con.close()


fund_pool_sql = """
CREATE TABLE `FundPool` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) DEFAULT NULL COMMENT '编号',
  `url` varchar(100) DEFAULT NULL COMMENT '迁移后数据表',
  `active` tinyint(1) DEFAULT '1' COMMENT '是否有效',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `write_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8 COMMENT='(''000000'', ''http://fund.eastmoney.com/000000.html'')';
"""

fund_detail_sql = """
CREATE TABLE `FundDetail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) DEFAULT '' COMMENT '编号',
  `name` varchar(20) DEFAULT NULL COMMENT '名称',
  `fund_type` varchar(40) DEFAULT NULL COMMENT '类型',
  `found_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '成立时间',
  `scale` float DEFAULT NULL COMMENT '规模，单位亿元',
  `fund_manager_url` varchar(100) DEFAULT NULL COMMENT '经理url',
  `fund_manager_name` varchar(20) DEFAULT NULL COMMENT '经理名称',
  `fund_admin` varchar(20) DEFAULT NULL COMMENT '管理人',
  `last_week_ranking` tinyint(4) DEFAULT NULL COMMENT '最近一周等级（1分：不佳，2分：一般，3分：良好，4分：优秀）',
  `last_month_ranking` tinyint(4) DEFAULT NULL COMMENT '最近一个月等级',
  `last_3months_ranking` tinyint(4) DEFAULT NULL COMMENT '最近三个月等级',
  `last_6months_ranking` tinyint(4) DEFAULT NULL COMMENT '最近六个月等级',
  `from_this_year_ranking` tinyint(4) DEFAULT NULL COMMENT '近一年来等级',
  `last_year_ranking` tinyint(4) DEFAULT NULL COMMENT '最近一年等级',
  `last_2years_ranking` tinyint(4) DEFAULT NULL COMMENT '最近两年等级',
  `last_3years_ranking` tinyint(4) DEFAULT NULL COMMENT '最近三年等级',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

fund_manager_sql = """
CREATE TABLE `FundManager` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) DEFAULT '' COMMENT '编号',
  `name` varchar(20) DEFAULT NULL COMMENT '名称',
  `url` varchar(100) DEFAULT NULL COMMENT 'url',
  `level` varchar(20) DEFAULT NULL COMMENT '星级',
  `start_date` date DEFAULT NULL COMMENT '任职起始日期',
  `capital_scala` float DEFAULT NULL COMMENT '管理规模，单位亿元',
  `fund_count` smallint(6) DEFAULT NULL COMMENT '管理基金数量',
  `score` float DEFAULT 0 COMMENT '综合评分',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `score` (`score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

if __name__ == '__main__':
    create_fund_pool()
