#include "stdafx.h"
#include<iostream>
#include<algorithm>
#include<cstdlib>
#include<cmath>
#include<string>
#include<cstring>
#include<vector>
#include<sstream>

using namespace std;

class item
{
public:
	double coef;
	int exp;
	item *link;
	item(double c, int e, item* l = NULL)
	{
		coef = c;
		exp = e;
		link = l;
	}
	item * add_after(double c, int e)
	{
		link = new item(c, e, this->link);
		return link;
	}
};

ostream & operator << (ostream & out, item * p)
{
	if (p->coef == 0)
		return out;
	else if (p->coef > 0)
		out << "+";
	else if (p->coef == -1)
		out << "-";
	if (p->exp == 0)
		out << p->coef;
	else if (p->coef != 1 && p->coef != -1)
		out << p->coef;
	switch (p->exp)
	{
	case 0:
		break;
	case 1:
		out << "X";
		break;
	default:
		out << "X^" << p->exp;
		break;
	}
	return out;
}

class polynomial
{
private:
	item *first;
public:
	polynomial()
	{
		first = new item(0,0);
	}

	polynomial(item * i)
	{
		first = new item(0,0);
		first = i;
	}

	polynomial(polynomial & p)
	{
		first = p.first;
	}

	~polynomial()
	{

	}

	item * get_head()
	{
		return first;
	}

	int get_size()
	{
		item *current = first;
		int cnt = 0;
		while (current->link != NULL)
		{
			current = current->link;
			cnt++;
		}
		return cnt;
	}

	void sort()
	{
		item * h = this->get_head()->link;
		while (h != NULL)
		{
			item * t = h->link;
			while (t != NULL)
			{
				if (t->exp > h->exp)
				{
					double c = t->coef;
					int e = t -> exp;
					t->coef = h->coef;
					t->exp = h->exp;
					h->coef = c;
					h->exp = e;
				}
				t = t->link;
			}
			h = h->link;
		}
	}

	void unrepeat()
	{
		this->sort();
		item *a = this->get_head()->link;
		item *b;
		while (a != NULL)
		{
			b = a->link;
			if (b == NULL)
				break;
			if (a->exp == b->exp)
			{
				a->coef += b->coef;
				a->link = b->link;
			}
			else
				a = b;
		}
	}

	int get_max_exp()
	{
		this->sort();
		if (first->link != NULL)
			return first->link->exp;
		else
			return 0;
	}

	double compute(double x)
	{
		double sum = 0;
		item *p = this->get_head()->link;
		while (p != NULL)
		{
			sum += p->coef * pow(x, p->exp);
			p = p -> link;
		}
		return sum;
	}

	polynomial derivative()
	{
		polynomial ans;
		item * scr = this->get_head()->link;
		item * des = ans.get_head();
		while (scr != NULL)
		{
			if (scr->coef * scr->exp != 0)
				des = des->add_after(scr->coef * scr->exp, scr->exp - 1);
			scr = scr->link;
		}
		return ans;
	}

};

istream & operator >>(istream & in,polynomial & p)
{
	item * rear = p.get_head();
	string temp;
	getline(in, temp);
	stringstream sstr;
	sstr << temp;
	double c;
	int e;
	while (sstr >> c >> e)
	{
		if (c != 0)
			rear = rear->add_after(c, e);
	}
	return in;
}

ostream & operator << (ostream & out,polynomial & p)
{
	p.sort();
	item * current = p.get_head()->link;
	if (current == NULL)
		out << 0;
	else
	{
		if (current->exp == 0)
			out << current->coef;
		else if (current->coef != 1 && current->coef != -1)
			out << current->coef;
		else if (current->coef == -1)
			out << "-";
		switch (current->exp)
		{
		case 0:
			break;
		case 1:
			out << "X";
			break;
		default:
			out << "X^" << current->exp;
			break;
		}
		current = current->link;
	}

	while (current != NULL)
	{
		out << current;
		current = current->link;
	}
	return out;
}

polynomial operator +(polynomial &a, polynomial &b)
{
	a.sort();
	b.sort();
	polynomial ans;
	item * pa = a.get_head()->link;
	item * pb = b.get_head()->link;
	item * pans =  ans.get_head();
	item * left;
	while (pa != NULL && pb != NULL)
	{
		if (pa->exp > pb->exp)
		{
			pans = pans->add_after(pa->coef, pa->exp);
			pa = pa->link;
		}
		else if (pa->exp < pb->exp)
		{
			pans = pans->add_after(pb->coef, pb->exp);
			pb = pb->link;
		}
		else if (pa->exp == pb->exp)
		{
			if (pa->coef + pb->coef != 0)
				pans = pans->add_after(pa->coef + pb->coef, pb->exp);
			pa = pa->link;
			pb = pb->link;
		}
	}
	if (pa != NULL)
		left = pa;
	else
		left = pb;
	while (left != NULL)
	{
		pans = pans->add_after(left->coef, left->exp);
		left = left->link;
	}
	return ans;
}

polynomial operator -(polynomial &a, polynomial &b)
{
	a.sort();
	b.sort();
	polynomial ans;
	item * pa = a.get_head()->link;
	item * pb = b.get_head()->link;
	item * pans = ans.get_head();
	item * left;
	while (pa != NULL && pb != NULL)
	{
		if (pa->exp > pb->exp)
		{
			pans = pans->add_after(pa->coef, pa->exp);
			pa = pa->link;
		}
		else if (pa->exp < pb->exp)
		{
			pans = pans->add_after(pb->coef, pb->exp);
			pb = pb->link;
		}
		else if (pa->exp == pb->exp)
		{
			if (pa->coef - pb->coef != 0)
				pans = pans->add_after(pa->coef - pb->coef, pb->exp);
			pa = pa->link;
			pb = pb->link;
		}
	}
	if (pa != NULL)
		left = pa;
	else
		left = pb;
	while (left != NULL)
	{
		pans = pans->add_after(left->coef, left->exp);
		left = left->link;
	}
	return ans;
}

polynomial operator *(polynomial &a, polynomial &b)
{
	polynomial ans;
	item *pa = a.get_head()->link;
	item *p = ans.get_head();
	while (pa != NULL)
	{
		item *pb = b.get_head()->link;
		while (pb != NULL)
		{
			int new_coef = pa->coef * pb->coef;
			if (new_coef != 0)
			{
				p = p->add_after(new_coef, pa->exp + pb->exp);
			}
			pb = pb->link;
		}
		pa = pa->link;
	}
	ans.unrepeat();
	return ans;
}

void print_menu()
{
	system("cls");
	cout << "--------- �򵥵Ķ���ʽ������ ---------" << endl;
	cout << "  1.��ʽ���              2.��ʽ���" << endl;
	cout << "  3.��ʽ���              4.һʽ��" << endl;
	cout << "  5.һʽ��ֵ              0.�˳�����" << endl;
	cout << "--------------------------------------" << endl;
	cout << "                 ___\b\b";
}

int main()
{
	print_menu();
	int choice;
	while (cin >> choice && choice != 0)
	{
		switch (choice)
		{
		case 1:
		{
				  cin.get();
				  polynomial a, b;
				  cout << "�밴��ϵ�� ָ�� ϵ�� ָ��������ʽ������Ҫ��ӵĶ���ʽ(һ������ʽ�Ի��н�������" << endl;
				  cin >> a >> b;
				  cout << "������Ķ���ʽ�ǣ�" << endl;
				  cout << a << endl << b << endl;
				  a.unrepeat();
				  b.unrepeat();
				  cout << "��ӽ��Ϊ��" << endl;
				  cout << a + b << endl;
				  cout << "��������ز˵���" << endl;
				  cin.get();
				  break;
		}
		case 2:
		{
				  cin.get();
				  polynomial a, b;
				  cout << "�밴��ϵ�� ָ�� ϵ�� ָ��������ʽ������Ҫ����Ķ���ʽ(һ������ʽ�Ի��н�������" << endl;
				  cin >> a >> b;
				  cout << "������Ķ���ʽ�ǣ�" << endl;
				  cout << a << endl << b << endl;
				  a.unrepeat();
				  b.unrepeat();
				  cout << "������Ϊ��" << endl;
				  cout << a - b << endl;
				  cout << "��������ز˵���" << endl;
				  cin.get();
				  break;
		}
		case 3:
		{
				  cin.get();
				  polynomial a, b;
				  cout << "�밴��ϵ�� ָ�� ϵ�� ָ��������ʽ������Ҫ��˵Ķ���ʽ(һ������ʽ�Ի��н�������" << endl;
				  cin >> a >> b;
				  cout << "������Ķ���ʽ�ǣ�" << endl;
				  cout << a << endl << b << endl;
				  a.unrepeat();
				  b.unrepeat();
				  cout << "��˽��Ϊ��" << endl;
				  cout << a * b << endl;
				  cout << "��������ز˵���" << endl;
				  cin.get();
				  break;
		}
		case 4:
		{
				  cin.get();
				  polynomial a;
				  cout << "�밴��ϵ�� ָ�� ϵ�� ָ��������ʽ������Ҫ�󵼵Ķ���ʽ(һ������ʽ�Ի��н�������" << endl;
				  cin >> a;
				  cout << "������Ķ���ʽ�ǣ�" << endl;
				  cout << a << endl;
				  a.unrepeat();
				  cout << "�󵼽��Ϊ��" << endl;
				  cout << a.derivative() << endl;
				  cout << "��������ز˵���" << endl;
				  cin.get();
				  break;
		}
		case 5:
		{
				  cin.get();
				  polynomial a;
				  int x;
				  cout << "�밴��ϵ�� ָ�� ϵ�� ָ��������ʽ������Ҫ��ֵ�Ķ���ʽ(һ������ʽ�Ի��н�������" << endl;
				  cin >> a;
				  cout << "������Ķ���ʽ�ǣ�" << endl;
				  cout << a << endl;
				  a.unrepeat();
				  cout << "�������������ֵx" << endl;
				  cin >> x;
				  cout << "��ֵ���Ϊ��" << endl;
				  cout << a.compute(x) << endl;
				  cout << "��������ز˵���" << endl;
				  cin.get();
				  cin.get();
				  break;
		}
		case 0:
		{
				  return 0;
		}
		default:
		{
				   cout << "���������������أ���";
				   cin.get();
				   break;
		}
		}
		print_menu();
	}
	return 0;
}


