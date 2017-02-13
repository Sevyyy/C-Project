package com.storm.loganalyze;

import java.util.HashMap;
import java.util.Map;
import java.io.PrintStream;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

public class ReportBolt extends BaseRichBolt {
	private Float totalMoney = (float) 0;
	private String user = "";
	private Float maxUserMoney = (float) 0;
	private String product = "";
	private Float maxProductMoney = (float) 0;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		// TODO Auto-generated method stub
		
	}

	public void execute(Tuple tuple) {
		// TODO Auto-generated method stub
		if (tuple.contains("user")) {
			Float money = tuple.getFloatByField("money");
			if (money > maxUserMoney) {
				this.user = tuple.getStringByField("user");
				maxUserMoney = money;
			}
		} else if (tuple.contains("product")){
			Float money = tuple.getFloatByField("money");
			if (money > maxProductMoney) {
				this.product = tuple.getStringByField("product");
				maxProductMoney = money;
			}
		} else if (tuple.contains("totalMoney")) {
			totalMoney = tuple.getFloatByField("totalMoney");
		}
		
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		// TODO Auto-generated method stub
		
	}

	public void cleanup() {
		PrintStream out = null;
		try {
			out = new PrintStream("output");
		} catch (Exception e) {
			System.out.println(e);
		}
		
		System.setOut(out);
		
		String str1 = String.format("%-8s%-10s%s", "用户ID", "商品类型", "销售总额");
		String str2 = String.format("%-10s%-14s%s", this.user, this.product, "total money");
		String str3 = String.format("%-10.2f%-14.2f%.2f", maxUserMoney, maxProductMoney, totalMoney);
		System.out.println(str1);
		System.out.println(str2);
		System.out.println(str3);
	}				
}
