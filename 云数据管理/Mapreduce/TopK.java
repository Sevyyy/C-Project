import java.io.IOException;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TopK {
	public static class TopKMapper extends
			Mapper<Object, Text, NullWritable, LongWritable> {
		public static final int K = 5;
		private TreeMap<Long, Long> treemap = new TreeMap<Long, Long>();

		protected void map(Object key, Text value, Context context)
				throws IOException {
			try {
				long k = Integer.parseInt(value.toString());
				treemap.put(k, k);
				if (treemap.size() > K) {
					treemap.remove(treemap.lastKey());
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		@Override
		protected void cleanup(Context context) throws IOException,
				InterruptedException {
			for (Long text : treemap.values()) {
				context.write(NullWritable.get(), new LongWritable(text));
			}
		}
	}

	public static class TopKReducer extends
			Reducer<NullWritable, LongWritable, NullWritable, LongWritable> {
		public static final int K = 5;
		private TreeMap<Long, Long> treemap = new TreeMap<Long, Long>();

		protected void reduce(NullWritable key, Iterable<LongWritable> values,
				Context context) throws IOException, InterruptedException {
			for (LongWritable value : values) {
				treemap.put(value.get(), value.get());
				if (treemap.size() > K) {
					treemap.remove(treemap.lastKey());
				}
			}
			for (Long val : treemap.navigableKeySet()) {
				context.write(NullWritable.get(), new LongWritable(val));
			}
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = { "hdfs://master:9000/input/input.txt",
				"hdfs://master:9000/output" };
		Job job = new Job(conf, "TopK"); 
		job.setJarByClass(TopK.class);
		job.setMapperClass(TopKMapper.class); 
		job.setReducerClass(TopKReducer.class); 
		job.setNumReduceTasks(1);
		job.setOutputKeyClass(NullWritable.class);  
		job.setOutputValueClass(LongWritable.class); 
		FileInputFormat.addInputPath(job, new Path(otherArgs[0])); 
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1); 
	}
}

