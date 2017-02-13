import org.apache.spark.{SparkConf, SparkContext}

object Fruit
{
	def main(args : Array[String])
	{
		val sparkConf = new SparkConf().setAppName("Fruit Count")
		val sc = new SparkContext(sparkConf)
		
		//read in the input text
		val textFile = sc.textFile("hdfs://master:9000/textFile")

		//map name:f1,f2... to (f1,(1,name)) (f2,(1,name))
		val name_fruits = textFile.flatMap(line => {
			val fields = line.split(":")
			fields(1).split(",").map(fruit => (fruit,(1,fields(0))))
			})

		//reduce by key and add the fruitcount as well as connect the name
		val fruit_count = name_fruits.reduceByKey((n1,n2) => (n1._1 + n2._1, n1._2 + ", " + n2._2))

		//sort the result after reduce and get the top1
		val sorted = fruit_count.map{
			case(f,(c,n)) => (c,(f,n));
		}.sortByKey(true, 1)
		val top1 = sorted.top(1)
		val top = top1(0)

		//print the result to console
		println("")
		println("Most popular fruit is " ++ top._2._1)
		println("Totally " ++ top._1.toString() ++ " people like it")
		println("Their name is: " ++ top._2._2)
		sc.parallelize(top1).saveAsTextFile("hdfs://master:9000/wq")
		println("Done")

		sc.stop();
	}
}