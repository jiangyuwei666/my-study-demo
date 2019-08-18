package com.sogou.spark

import org.apache.spark.{SparkConf, SparkContext}

object WordCount {
  def main(args: Array[String]): Unit = {
    // 创建spark配置
    val conf = new SparkConf().setAppName("WordCount")
    // 创建spark执行的入口
    val sc = new SparkContext(conf)
    // 指定以后从哪里读取数据创建RDD（弹性分布式数据集）
    //    val lines:RDD[String] = sc.textFile(args(0)).flatMap(_.split(" ")).map((_,1)).reduceByKey()

    val lines = sc.textFile(args(0)) //hdfs://SunshineNameNode2/user/tupu_spark/jiangyuwei
    // 切分压平
    val words = lines.flatMap(_.split(" ")) // _表示一行内容，把每一行内容取出来
    // 将单词和1组合
    val wordAndOne = words.map((_, 1))
    // 按key 进行聚合
    val reduced = wordAndOne.reduceByKey(_ + _)
    // 排序
    val sorted = reduced.sortBy(_._2, false)
    // 将结果保存到HDFS中
    sorted.saveAsTextFile(args(1))
  }
}
