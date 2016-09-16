package com.ezdi.poc.dao;

import java.util.List;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.ezdi.poc.beans.Dummy;

@Component
public class DummyDao {
	
	@Autowired
	private SessionFactory sessionFactory;
	
	
	//SAMPLE ::: SELECT distinct D.str3 where D.num1=:num1 and D.num2=:num2 
	//							and D.num3=:num3 and D.str1=:str1 and D.str2=:str2
	@Value("${hql.permission.query}")
	private String HQL_PERMISSION_QUERY;
	
	
	//SAMPLE ::: FROM Dummy
	@Value("${hql.selectall.query}")
	private String HQL_SELECT_ALL_QUERY;
	
	
	public void display(){
		System.out.println("DUMMYDAO:: permission-query: "+HQL_PERMISSION_QUERY);
		System.out.println("DUMMYDAO:: select-all-query: "+HQL_SELECT_ALL_QUERY);
	}
	
	public List<String> findPermissionSet(List<Integer> nums, List<String> strs){
		
		Session session = sessionFactory.openSession();
		Query query = session.createQuery(HQL_PERMISSION_QUERY);
		for(int i=0; i<nums.size(); i++){
			query.setParameter("num"+(i+1), nums.get(i));
		}
		for(int i=0; i<strs.size(); i++){
			query.setParameter("str"+(i+1), strs.get(i));
		}
		List<String> ret = query.list();
		session.close();
		return ret;
	}
	
	public List<String> findPermissionSet(Dummy dummy){
		Session session = sessionFactory.openSession();
		Query query = session.createQuery(HQL_PERMISSION_QUERY).setProperties(dummy);
		List<String> ret = query.list();
		session.close();
		return ret;
	}
	
	public List<Dummy> getAll(){
		Session session = sessionFactory.openSession();
		Query query = session.createQuery(HQL_SELECT_ALL_QUERY);
		List<Dummy> ret = query.list();
		session.close();
		return ret;
	}
}
