import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import java.io.IOException;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

/**
 * Created by dqd on 2016/10/30.
 */
public class TK {

    private static class TKMapper extends Mapper<LongWritable, Text, Text, Text> {

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            int K = 5;
            PriorityQueue<Integer> priorityQueue = new PriorityQueue<Integer>(K, new Comparator<Integer>() {
                public int compare(Integer o1, Integer o2) {
                    return o2.compareTo(o1);
                }
            });
            StringTokenizer st = new StringTokenizer(value.toString());
            while (st.hasMoreTokens()) {
                String element = st.nextToken();
                Integer tmp = Integer.parseInt(element);
                priorityQueue.add(tmp);
                if (priorityQueue.size() > 5) {
                    priorityQueue.poll();
                }
            }
            Text outKey = new Text();
            outKey.set("tk");
            StringBuffer sb = new StringBuffer();
            while (!priorityQueue.isEmpty()) {
                sb.append(String.valueOf(priorityQueue.poll() + ","));
            }
            Text outVal = new Text(sb.toString());
            context.write(outKey, outVal);
        }
    }

    private static class TKReducer extends Reducer<Text, Text , Text, IntWritable>    {
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            int K = 5;
            PriorityQueue<Integer> priorityQueue = new PriorityQueue<Integer>(K, new Comparator<Integer>() {
                public int compare(Integer o1, Integer o2) {
                    return o2.compareTo(o1);
                }
            });
            for (Text value : values) {
                String kInt = value.toString();
                String[] ss = kInt.split(",");  // length must be 5
                for(String tmp : ss){
                    priorityQueue.add(Integer.parseInt(tmp));
                    if (priorityQueue.size() > 5) {
                        priorityQueue.poll();
                    }
                }
            }

            for(int i =0; i<K;i++){
                String outKey =  "# "+ (i+1) +": ";
                IntWritable outVal = new IntWritable(priorityQueue.poll());
                context.write(new Text(outKey), outVal);
            }

        }
    }

        public static void main(String[] args) throws Exception{
            Configuration conf = new Configuration();
            String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
            if (otherArgs.length < 2) {
                System.err.println("Usage: wordcount <in> [<in>...] <out>");
                System.exit(2);
            }
            Job job = new Job(conf, "TK");
            job.setJarByClass(TK.class);
            job.setMapperClass(TKMapper.class);
            job.setReducerClass(TKReducer.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);
            FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
            FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
            System.exit(job.waitForCompletion(true) ? 0 : 1);
        }
}

