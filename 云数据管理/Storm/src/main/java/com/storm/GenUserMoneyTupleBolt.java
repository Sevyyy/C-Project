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

public class GenUserMoneyTupleBolt extends BaseRichBolt {

	private OutputCollector collector;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		// TODO Auto-generated method stub
		this.collector = collector;
	}

	public void execute(Tuple tuple) {
		// TODO Auto-generated method stub
		String record = tuple.getStringByField("record");
		String[] attrs = record.split(",");
		this.collector.emit(new Values(attrs[0], Float.parseFloat(attrs[2])));
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		// TODO Auto-generated method stub
		declarer.declare(new Fields("user","money"));
	}
			
}
