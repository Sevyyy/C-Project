package com.storm.loganalyze;

import java.util.Map;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

public class RecordSpout extends BaseRichSpout {
	private SpoutOutputCollector collector;
	// 用户ID，商品类型，金额
	private String[] records = {
		"10000,clothing,123.2",
		"10001,computer,365.8",
		"10002,phone,127.3",
		"10003,shoe,965.45",
		"10004,snacks,548.7",
		"10000,clothing,1000",
		"10005,shoe,666",
		"10001,computer,365.8",
		"10002,phone,127.3",
		"10003,shoe,965.45"
	};
	private int index = 0;

	public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
		// TODO Auto-generated method stub
		this.collector = collector;
	}

	public void nextTuple() {
		// TODO Auto-generated method stub
		while (index < records.length) {
			this.collector.emit(new Values(records[index]));
			index++;
		}
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		// TODO Auto-generated method stub
		declarer.declare(new Fields("record"));
	}
}
