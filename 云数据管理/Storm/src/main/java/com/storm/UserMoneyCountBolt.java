package com.storm.loganalyze;

import java.util.HashMap;
import java.util.Map;
import java.io.PrintStream;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

public class UserMoneyCountBolt extends BaseRichBolt {

	private OutputCollector collector;
	private HashMap<String, Float> counts = null;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		// TODO Auto-generated method stub
		this.collector = collector;
		this.counts = new HashMap<String, Float>();
	}

	public void execute(Tuple tuple) {
		// TODO Auto-generated method stub
		String user = tuple.getStringByField("user");
		Float money = tuple.getFloatByField("money");
		Float all_money = this.counts.get(user);
		if(all_money == null)
		{
			all_money = (float)0;
		}
		all_money += money;
		this.counts.put(user, all_money);
		this.collector.emit(new Values(user, all_money));
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		// TODO Auto-generated method stub
		declarer.declare(new Fields("user","money"));
	}
			
}
