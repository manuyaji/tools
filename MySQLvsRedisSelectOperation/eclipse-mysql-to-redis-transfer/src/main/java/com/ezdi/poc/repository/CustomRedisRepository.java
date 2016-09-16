package com.ezdi.poc.repository;

import java.util.Calendar;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class CustomRedisRepository {
	
	@Autowired
	private RedisTemplate<String, Object> redisTemplate;
	
	public Set<String> getAllKeysOfPattern(String pattern){
		return redisTemplate.keys(pattern);
	}
	
	public void delete(String key){
		redisTemplate.delete(key);
	}
	
	public void delete(Collection<String> keys){
		redisTemplate.delete(keys);
	}
	
	public boolean keyExists(String key){
		return redisTemplate.hasKey(key);
	}
	
	public boolean hashFieldExists(String key,String hashKey){
		return redisTemplate.boundHashOps(key).hasKey(hashKey);
	}
	
	public String getValueAsString(String key){
		return (String)getValueAsObject(key);
	}
	
	public Object getValueAsObject(String key){
		return redisTemplate.boundValueOps(key).get();
	}
	
	public String getHashFieldValueAsString(String key, String hashKey){
		return (String)getHashFieldValueAsObject(key, hashKey);
	}
	
	public Object getHashFieldValueAsObject(String key, String hashKey){
		return redisTemplate.boundHashOps(key).get(hashKey);
	}
	
	public void set(String key, Object value){
		redisTemplate.boundValueOps(key).set(value);
	}
	
	public void setWithExpire(String key, Object value, Date expireAt){
		long curMilliSeconds = Calendar.getInstance().getTime().getTime();
		long expireAtMilliSeconds = expireAt.getTime();
		setWithExpire(key, value, (expireAtMilliSeconds - curMilliSeconds), TimeUnit.MILLISECONDS);
	}
	
	public void setWithExpire(String key, Object value, long timeOutInSeconds){
		setWithExpire(key, value, timeOutInSeconds, TimeUnit.SECONDS);
	}
	
	public void setWithExpire(String key, Object value, long timeOut, TimeUnit timeUnit){
		redisTemplate.boundValueOps(key).set(value, timeOut, timeUnit);
	}
	
	public void setHashField(String key, String hashKey, Object value){
		redisTemplate.boundHashOps(key).put(hashKey, value);
	}
	
	public void setHashFieldWithExpire(String key, String hashKey, Object value, Date expireAt){
		redisTemplate.boundHashOps(key).put(hashKey, value);
		redisTemplate.boundHashOps(key).expireAt(expireAt);
	}
	
	public void setHashFieldWithExpire(String key, String hashKey, Object value, long timeOutInSeconds){
		setHashFieldWithExpire(key, hashKey, value, timeOutInSeconds, TimeUnit.SECONDS);
	}
	
	public void setHashFieldWithExpire(String key, String hashKey, Object value, long timeOut, TimeUnit timeUnit){
		redisTemplate.boundHashOps(key).put(hashKey, value);
		redisTemplate.boundHashOps(key).expire(timeOut, timeUnit);
	}
	
	public void setHashMap(String key, HashMap<? extends Object, ? extends Object> hashMap){
		redisTemplate.boundHashOps(key).putAll(hashMap);
	}
	
	public void setHashMapWithExpire(String key, HashMap<? extends Object, ? extends Object> hashMap, Date expireAt){
		redisTemplate.boundHashOps(key).putAll(hashMap);
		redisTemplate.boundHashOps(key).expireAt(expireAt);
	}
	
	public void setHashMapWithExpire(String key, HashMap<? extends Object, ? extends Object> hashMap, long timeOutInSeconds){
		setHashMapWithExpire(key, hashMap, timeOutInSeconds, TimeUnit.SECONDS);
	}
	
	public void setHashMapWithExpire(String key, HashMap<? extends Object, ? extends Object> hashMap, long timeOut, TimeUnit unit){
		redisTemplate.boundHashOps(key).putAll(hashMap);
		redisTemplate.boundHashOps(key).expire(timeOut, unit);
	}
	
	public void expire(String key, long timeOut, TimeUnit unit){
		redisTemplate.boundValueOps(key).expire(timeOut, unit);
	}
	
	public void expire(String key, long timeOutInSeconds){
		expire(key, timeOutInSeconds, TimeUnit.SECONDS);
	}
	
	public void expireAt(String key, Date expireAt){
		redisTemplate.expireAt(key, expireAt);
	}
	
	public void add(String key, Object...values){
		redisTemplate.boundSetOps(key).add(values);
	}
		
	public void addWithExpire(String key, Date expireAt, Object...values){
		redisTemplate.boundSetOps(key).add(values);
		redisTemplate.boundSetOps(key).expireAt(expireAt);
	}
	
	public void addWithExpire(String key, long timeOutInSeconds,  Object...values){
		redisTemplate.boundSetOps(key).add(values);
		redisTemplate.boundSetOps(key).expire(timeOutInSeconds, TimeUnit.SECONDS);
	}
	
	public void addWithExpire(String key, long timeOut, TimeUnit unit,  Object...values){
		redisTemplate.boundSetOps(key).add(values);
		redisTemplate.boundSetOps(key).expire(timeOut, unit);
	}
	
	public Set<Object> getSetMembers(String key){
		return redisTemplate.boundSetOps(key).members();
	}
}
