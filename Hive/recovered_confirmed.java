package com.pae.hive.udf;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public final class recovered_confirmed extends UDF {
	/*
	public Text evaluate(final Text s) {
		if (s == null) { return null; }
		return new Text(s.toString().replaceAll("^\"|\"$", ""));
	}
    */

    public float evaluate(int a, int b) { 
		float resultado = (float)a/b;
			return resultado; 
		} 
	}