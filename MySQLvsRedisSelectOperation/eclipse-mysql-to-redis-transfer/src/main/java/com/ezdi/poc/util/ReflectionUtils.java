package com.ezdi.poc.util;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;

import javax.persistence.Column;

import org.springframework.util.StringUtils;

public class ReflectionUtils {
	
	public static HashMap<String, Object> getDatabaseModelObjectFieldValueMap(Object dbModel) throws IllegalAccessException{
		HashMap<String, Object> fieldMap = new HashMap<>();
		Class clazz = dbModel.getClass();
		Field fields[] = clazz.getDeclaredFields();
		for(Field each : fields){
			Column column = each.getDeclaredAnnotation(Column.class);
			fieldMap.put(column.name(), each.get(dbModel));
		}
		return fieldMap;
	}
	
	public static boolean setValue(String fieldName, Object object, Object valueToSet){
		Class clazz = object.getClass();
		try{
			clazz.getDeclaredField(fieldName).set(object, valueToSet);
		}
		catch(IllegalAccessException i){
			try{
				invokeSetter(fieldName, object, valueToSet);
			}
			catch(Exception e){
				return true;
			}
		}
		catch(NoSuchFieldException n){
			return true;
		}
		return true;
	}
	
	public static Object returnValue(String fieldName, Object object){
		Class clazz = object.getClass();
		Object ret=null;
		try{
			ret = clazz.getDeclaredField(fieldName).get(object);			
		}
		catch(IllegalAccessException i){
			try{
				ret = invokeGetter(fieldName, object);
			}
			catch(Exception e){
				return null;
			}
		}
		catch(NoSuchFieldException n){
			return null;
		}
		return ret;
	}
	
	public static Object invokeGetter(String fieldName, Object object) throws NoSuchMethodException, 
			IllegalAccessException, InvocationTargetException{
		Object ret = null;
		Class clazz = object.getClass();
		Method methodToInvoke = clazz.getMethod(getterMethodName(fieldName));
		ret = methodToInvoke.invoke(object);
		return ret;
	}
	
	public static String getterMethodName(String fieldName){
		if(fieldName == null || fieldName.length() == 0) return null;
		String ret = "get"+StringUtils.capitalize(fieldName);
		return ret;
	}
	
	public static String setterMethodName(String fieldName){
		if(fieldName == null || fieldName.length() == 0) return null;
		String ret = "set"+StringUtils.capitalize(fieldName);
		return ret;
	}
	
	public static void invokeSetter(String fieldName, Object object, Object ...params)throws NoSuchMethodException, 
			IllegalAccessException, InvocationTargetException{
		Class clazz = object.getClass();
		Method methodToInvoke = clazz.getMethod(setterMethodName(fieldName));
		methodToInvoke.invoke(object, params);
	}

}
