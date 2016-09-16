package com.ezdi.poc.util;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ThreadLocalRandom;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.ezdi.poc.beans.Dummy;
import com.ezdi.poc.dao.DummyDao;
import com.ezdi.poc.repository.CustomRedisRepository;

@Component
public class MainRunner {
	
	@Autowired
	private CustomRedisRepository redisRepository;
	
	@Autowired
	private DummyDao dummyDao;
	
	@Value("${database.columns.integer}")
	private int numCols;
	
	@Value("${database.columns.string}")
	private int strCols;
	
	@Value("${database.columns.values}")
	private int values;
	
	@Value("${num.test.cases}")
	private int testCases=100;
	
	@Value("${num.select.queries}")
	private int numSelectQueries=100;
	
	private ThreadLocalRandom rnd = ThreadLocalRandom.current();
	
	private List<List<String>> mysqlResultList = new ArrayList<>();
	private List<Set<Object>> redisResultList = new ArrayList<>();
	
	public void display(boolean isDisplayDummyDao){
		System.out.println("MAINRUNNER:: numCols: "+numCols);
		System.out.println("MAINRUNNER:: strCols: "+strCols);
		if(isDisplayDummyDao){
			dummyDao.display();
		}
	}
	
	public void transferFromMysqlToRedis(){
		List<Dummy> dummyList = dummyDao.getAll();
		for(Dummy each: dummyList){
			createAndPutIntoRedis(each);
		}
	}
	
	private void createAndPutIntoRedis(Dummy dummy){
		String redisValue = (String)ReflectionUtils.returnValue("str"+strCols, dummy);
		redisRepository.add(makeRedisKey(dummy), redisValue);
	}
	
	public List<Dummy> createSelectQueries(int numOfQueries){
		if(numOfQueries <= 0) numOfQueries = 10000;
		ArrayList<Dummy> list = new ArrayList<>();
		for(int i=0; i<numOfQueries; i++){
			Dummy dummy = createRandomDummy();
			list.add(dummy);
		}
		return list;
	}
	
	private Dummy createRandomDummy(){
		Dummy ret = new Dummy();
		int val=0;
		for(int i=1; i<=numCols;i++){
			val = rnd.nextInt(values)+1;
			Integer intVal = val;
			ReflectionUtils.setValue("num"+i, ret, intVal);
		}
		for(int i=1; i<=strCols-1; i++){
			val = rnd.nextInt(values)+1;
			String strVal = "str"+i+"_"+val;
			ReflectionUtils.setValue("str"+i, ret, strVal);
		}
		return ret;
	}
	
	public long executeQueriesInMySQL(List<Dummy> list){
		long start = System.currentTimeMillis();
		for(Dummy each: list){
			mysqlResultList.add(dummyDao.findPermissionSet(each));
		}
		long end = System.currentTimeMillis();
		return (end - start);
	}
	
	public long executeQueriesInRedis(List<Dummy> list){
		long start = System.currentTimeMillis();
		for(Dummy each: list){
			redisResultList.add(redisRepository.getSetMembers(makeRedisKey(each)));
		}
		long end = System.currentTimeMillis();
		return (end - start);
	}
	
	private String makeRedisKey(Dummy dummy){
		StringBuilder stringBuilder = new StringBuilder();
		boolean isAppendNeeded=false;
		for(int i=1; i<=numCols;i++){
			if(isAppendNeeded){
				stringBuilder.append(":");
			}
			int x = (Integer)ReflectionUtils.returnValue("num"+i, dummy);
			stringBuilder.append(String.valueOf(x));
			if(!isAppendNeeded) isAppendNeeded=true;
		}
		for(int i=1; i<=strCols-1;i++){
			if(isAppendNeeded){
				stringBuilder.append(":");
			}
			String x = (String)ReflectionUtils.returnValue("str"+i, dummy);
			stringBuilder.append(x);
		}
		String redisKey = stringBuilder.toString();
		return redisKey;
	}
	
	public boolean areResultsOfQueriesSame(){
		int len=0;
		if((len=mysqlResultList.size()) != redisResultList.size()){
			return false;
		}
		for(int i=0; i<len; i++){
			List<String> mysqlResult = mysqlResultList.get(i);
			Set<Object> mysqlSet = new HashSet<>();
			mysqlSet.addAll(mysqlResult);
			Set<Object> redisResult  = redisResultList.get(i);
			if(!redisResult.equals(mysqlSet)){
				return false;
			}
		}
		return true;
	}

	public int getTestCases() {
		return testCases;
	}

	public void setTestCases(int testCases) {
		this.testCases = testCases;
	}

	public int getNumSelectQueries() {
		return numSelectQueries;
	}

	public void setNumSelectQueries(int numSelectQueries) {
		this.numSelectQueries = numSelectQueries;
	}

}
