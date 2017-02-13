package com.storm.loganalyze;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.tuple.Fields;


public class LogAnalyzeTopology {
	private static final String RECORD_SPOUT_ID = "record-spout";
	private static final String GENPRODUCTMONEYTUPLE_BOLT_ID = "genProductMoneyTuple-bolt";
	private static final String GENUSERMONEYTUPLE_BOLT_ID = "genUserMoneyTuple-bolt";
	private static final String PRODUCTMONEYCOUNT_BOLT_ID = "ProductMoneyCount-bolt";
	private static final String USERMONEYCOUNT_BOLT_ID = "UserMoneyCount-bolt";
	private static final String TOTALMONEYCOUNT_BOLT_ID = "TotalMoneyCount-bolt";
	private static final String REPORT_BOLT_ID = "report-bolt";
	private static final String TOPOLOGY_NAME = "log-analyze-topology";

	public static void main(String[] args) throws Exception {

		RecordSpout recordSpout = new RecordSpout();
		GenProductMoneyTupleBolt genProductMoneyTupleBolt = new GenProductMoneyTupleBolt();
		GenUserMoneyTupleBolt genUserMoneyTupleBolt = new GenUserMoneyTupleBolt();
	 	ProductMoneyCountBolt productMoneyCountBolt = new ProductMoneyCountBolt();
	 	UserMoneyCountBolt userMoneyCountBolt = new UserMoneyCountBolt();
	 	TotalMoneyCount totalMoneyCount = new TotalMoneyCount();
		ReportBolt reportBolt = new ReportBolt();

	 	TopologyBuilder builder = new TopologyBuilder();

	 	builder.setSpout(RECORD_SPOUT_ID, recordSpout);
	 	builder.setBolt(GENPRODUCTMONEYTUPLE_BOLT_ID, genProductMoneyTupleBolt)
	 		.shuffleGrouping(RECORD_SPOUT_ID);
	 	builder.setBolt(GENUSERMONEYTUPLE_BOLT_ID, genUserMoneyTupleBolt)
	 		.shuffleGrouping(RECORD_SPOUT_ID);
	 	builder.setBolt(TOTALMONEYCOUNT_BOLT_ID, totalMoneyCount)
	 		.shuffleGrouping(RECORD_SPOUT_ID);
	 	builder.setBolt(PRODUCTMONEYCOUNT_BOLT_ID, productMoneyCountBolt)
	 		.fieldsGrouping(GENPRODUCTMONEYTUPLE_BOLT_ID, new Fields("product"));
	 	builder.setBolt(USERMONEYCOUNT_BOLT_ID, userMoneyCountBolt)
	 		.fieldsGrouping(GENUSERMONEYTUPLE_BOLT_ID, new Fields("user"));
	 	builder.setBolt(REPORT_BOLT_ID, reportBolt)
	 		.globalGrouping(TOTALMONEYCOUNT_BOLT_ID)
	 		.globalGrouping(PRODUCTMONEYCOUNT_BOLT_ID)
 			.globalGrouping(USERMONEYCOUNT_BOLT_ID);

	 	Config config = new Config();

	 	if (args.length == 0) {
	 		LocalCluster cluster = new LocalCluster();
	 		cluster.submitTopology(TOPOLOGY_NAME, config, builder.createTopology());
	 		waitForSeconds(30);
	 		cluster.killTopology(TOPOLOGY_NAME);
	 		cluster.shutdown();
	 		} else {
	 			StormSubmitter.submitTopology(args[0], config, builder.createTopology());
	 		}
		}
	private static void waitForSeconds(int seconds) {
		// TODO Auto-generated method stub
		try {
			Thread.sleep(seconds * 1000);
		} catch (InterruptedException e) {
		}

	}
}
