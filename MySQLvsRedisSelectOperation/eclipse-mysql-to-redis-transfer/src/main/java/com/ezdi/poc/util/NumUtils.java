package com.ezdi.poc.util;

public class NumUtils {
	
	public static long average(long[] arr){
		long sum = 0;
		for(long each: arr){
			sum += each;
		}
		return sum/(arr.length);
	}
}
