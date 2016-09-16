package com.ezdi.poc;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import com.ezdi.poc.beans.Dummy;
import com.ezdi.poc.util.MainRunner;
import com.ezdi.poc.util.NumUtils;

@SpringBootApplication
public class MysqlToRedisPoCApplication { 
	
	public static void main(String args[]){
		ApplicationContext appContext =SpringApplication.run(MysqlToRedisPoCApplication.class, args);
		String[] beanNames = appContext.getBeanDefinitionNames();
        System.out.println("The beans configured (automatically by spring-boot!!) are: ");
        if(beanNames != null){
            System.out.println("NUMBER : "+beanNames.length);
            Arrays.sort(beanNames);
            for(String each: beanNames){
                System.out.println(each);
            }
        }
        else{
            System.out.println("beanNames is NULL");
        }
        
        MainRunner mainRunner = appContext.getBean(MainRunner.class);
        mainRunner.display(true);
        mainRunner.transferFromMysqlToRedis();
        
        int testCases = mainRunner.getTestCases();
        int selectQueries=mainRunner.getNumSelectQueries();
        
        long[] mysqlTimes = new long[testCases];
        long[] redisTimes = new long[testCases];
        
        for(int i=0; i<testCases; i++){
        	List<Dummy> queryListDummy = mainRunner.createSelectQueries(selectQueries);
        	mysqlTimes[i] = mainRunner.executeQueriesInMySQL(queryListDummy);
        	redisTimes[i] = mainRunner.executeQueriesInRedis(queryListDummy);
        }
        
        if(mainRunner.areResultsOfQueriesSame()){
        	System.out.println("THANK GOD!! RESULTS ARE THE SAME!!");
        }
        else{
        	System.out.println("AYYAYYOOOO!! RESULTS ARE NOT THE SAME :-(");
        }
        
        for(int i=0; i<testCases; i++){
        	System.out.println("mysqlTime: "+mysqlTimes[i]+"\t redisTime: "+redisTimes[i]);
        }
        
        System.out.println("MySQL Average: "+NumUtils.average(mysqlTimes));
        System.out.println("Redis Average: "+NumUtils.average(redisTimes));
	}

}
