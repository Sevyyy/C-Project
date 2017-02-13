import java.io.IOException;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class TopK {
	public static class TokenizerMapper
			extends Mapper<Object, Text, NullWritable, Text>{
		private final static int len = 5;
		private TreeMap<Integer,Integer> m = new TreeMap<Integer,Integer>();
		@Override
		public void map(Object key, Text values, Context context)
			throws IOException, InterruptedException {
				Integer num = Integer.parseInt(values.toString());
				m.put(num,num);
				try{
					if(m.size() > len){
					m.remove(m.lastKey());
					}
				}catch(Exception e){
					e.printStackTrace();
				}
				StringBuffer sb = new StringBuffer();
				for(Integer value:m.values()){
					String tmp = String.valueOf(value);
					sb.append(tmp+"/");
				}
				context.write(NullWritable.get(),new Text(sb.toString()));			
			}
	}

	public static class IntMinReducer
			extends Reducer<NullWritable, Text,NullWritable,LongWritable>{
		private static int len = 5;
		private TreeMap<Integer,Integer> resultMap = new TreeMap<Integer,Integer>();
		@Override
		public void reduce(NullWritable key, Iterable<Text> values, Context context)
			throws IOException, InterruptedException{
		//	String tmp = new String();
			for(Text value : values){
				String kInt = value.toString();
				String[] ss = kInt.split("/");  // length must be 5
				for(String tmp : ss){	
					resultMap.put(Integer.parseInt(tmp),Integer.parseInt(tmp));
					try{
						if(resultMap.size() > len){
						resultMap.remove(resultMap.lastKey());
						}
					}catch(Exception e){
						e.printStackTrace();
					}
				}
			}
			for(Integer value : resultMap.values()){
				context.write(NullWritable.get(),new LongWritable(value));
			}
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();		
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    		
		if (otherArgs.length < 2) {
                System.err.println("Usage: wordcount <in> [<in>...] <out>");
                System.exit(2);
            	}
		
		Job job = Job.getInstance(conf,"topK");
		job.setJarByClass(TopK.class);
        	job.setMapperClass(TokenizerMapper.class);

		job.setMapOutputKeyClass(NullWritable.class);
		job.setMapOutputValueClass(Text.class);

        	job.setReducerClass(IntMinReducer.class);
        	job.setOutputKeyClass(NullWritable.class);
        	job.setOutputValueClass(IntWritable.class);

        	FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        	FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        	System.exit(job.waitForCompletion(true) ? 0 : 1);

	}

}
