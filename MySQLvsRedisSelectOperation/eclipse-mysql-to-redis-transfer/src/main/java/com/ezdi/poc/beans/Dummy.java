package com.ezdi.poc.beans;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name="dummy")
public class Dummy {
	
	@Id
	@Column(name="id")
	private int id;
	
	@Column(name="num1")
	private int num1;
	
	@Column(name="num2")
	private int num2;
	
	@Column(name="num3")
	private int num3;
	
	@Column(name="num4")
	private int num4;
	
	
	@Column(name="str1")
	private String str1;
	
	@Column(name="str2")
	private String str2;
	
	@Column(name="str3")
	private String str3;
	
	@Column(name="str4")
	private String str4;

	@Column(name="str5")
	private String str5;
	
	@Column(name="str6")
	private String str6;
	
	@Column(name="str7")
	private String str7;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public int getNum1() {
		return num1;
	}

	public void setNum1(int num1) {
		this.num1 = num1;
	}

	public int getNum2() {
		return num2;
	}

	public void setNum2(int num2) {
		this.num2 = num2;
	}

	public int getNum3() {
		return num3;
	}

	public void setNum3(int num3) {
		this.num3 = num3;
	}

	public int getNum4() {
		return num4;
	}

	public void setNum4(int num4) {
		this.num4 = num4;
	}

	public String getStr1() {
		return str1;
	}

	public void setStr1(String str1) {
		this.str1 = str1;
	}

	public String getStr2() {
		return str2;
	}

	public void setStr2(String str2) {
		this.str2 = str2;
	}

	public String getStr3() {
		return str3;
	}

	public void setStr3(String str3) {
		this.str3 = str3;
	}
	
	public String getStr4() {
		return str4;
	}

	public void setStr4(String str4) {
		this.str4 = str4;
	}

	public String getStr5() {
		return str5;
	}

	public void setStr5(String str5) {
		this.str5 = str5;
	}

	public String getStr6() {
		return str6;
	}

	public void setStr6(String str6) {
		this.str6 = str6;
	}

	public String getStr7() {
		return str7;
	}

	public void setStr7(String str7) {
		this.str7 = str7;
	}
	
}
