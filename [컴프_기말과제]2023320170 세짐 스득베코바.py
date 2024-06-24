import matplotlib.pyplot as plt

def fun_input():
    try:
        salary, pocket_money = map(int, input("본인의 월급과 용돈 각각의 금액을 입력해 주십시오: ").split())
        monthly_rent = int(input("월세 금액: "))
        sen_meeting_cnt = int(input("이번 달에 선배와의 밥약 개수: "))
        jun_meeting_cnt = int(input("이번 달에 후배와의 밥약 개수: "))
        transport_count = int(input("보통 한 달에 대중교통 활용 개수: "))
    except ValueError:
        print("입력이 올바르지 않습니다. 다시 시도해 주십시오.")
        return fun_input()

    salary -= monthly_rent
    return [salary, pocket_money, sen_meeting_cnt, jun_meeting_cnt, transport_count]  # 예외 처리를 포함한 입력 함수

def fun_salary(salary, sen_meeting_cnt, jun_meeting_cnt, transport_count):  # 월급을 사용하는 소비
    salary_savings = salary * 0.05
    living_expenses = salary * 0.25
    meal_expenses = salary * 0.45
    transportation_expenses = salary * 0.25
    rest_meeting_exp = 0
    
    sen_meeting_exp = sen_meeting_cnt * 13000  # 선배와의 밥약일 경우 13.0원 (커피값)
    jun_meeting_exp = jun_meeting_cnt * 25000  # 후배와의 밥약일 경우 25.0원 (밥값)
    total_meeting_exp = sen_meeting_exp + jun_meeting_exp


    if total_meeting_exp <= meal_expenses:  # 밥약에 드는 비용이 식비를 넘는 경우 예외처리
        groceries = meal_expenses - total_meeting_exp
    else:
        groceries = 0
        rest_meeting_exp += total_meeting_exp - meal_expenses

        transport_count =  transport_count * 1600        # 대중 교통을 사용하는 개수를 기본 요금에 곱하고 1달에 필요한 교통비 구함
    if transport_count > transportation_expenses:
        transport_count = (transport_count - transportation_expenses) / 1600        # 한달에 필요한 교통비가 사용자에게 있는 금액을 넘으면 몇번 걸어가야 하는지 계산
        print("교통비 = ", int(transportation_expenses))
        print(int(transport_count), "번 걸어야 합니다ㅠㅠ")
    else:
        print("교통비 = ", int(transportation_expenses), "원")  # 교통비 계산

    print(f"생활비 = {int(living_expenses)}원")
    print(f"선배와의 밥약 비용 = {int(sen_meeting_exp)}원")
    print(f"후배와의 밥약 비용 = {int(jun_meeting_exp)}원")
    print(f"식비 = {int(groceries)}원")
    print(f"교통비 = {int(transport_cost)}원")
    print(f"저금 = {int(salary_savings)}원")
        
    return rest_meeting_exp, salary_savings, living_expenses, meal_expenses, groceries, transport_cost

def fun_pocket_money(pocket_money, rest_meeting_exp):       # 용돈 계산 함수
    pocket_money += rest_meeting_exp  # 남은 월급을 용돈에 추가
    drinks = pocket_money * 0.5
    etc = pocket_money * 0.5

    while (etc - rest_meeting_exp) < 0:     # 밥약 비용이 넘칠 경우 밥약 줄임
        meeting_type = input("밥약을 줄일 대상 (선배/후배): ")
        if meeting_type == "선배":
            eat_out_meeting = int(input("선배와의 밥약 개수를 줄이세요: "))
            rest_meeting_exp = eat_out_meeting * 13000
            print(f"선배와의 밥약 비용 = {int(rest_meeting_exp)}원")
        elif meeting_type == "후배":
            eat_out_meeting = int(input("후배와의 밥약 개수를 줄이세요: "))
            rest_meeting_exp = eat_out_meeting * 25000
            print(f"선배와의 밥약 비용 = {int(rest_meeting_exp)}원")
        else:
            print("잘못된 입력입니다. '선배' 또는 '후배'를 입력해 주세요.")
            continue
        etc -= rest_meeting_exp

    print(f"음료 = {int(drinks)}원")
    print(f"기타 소비 = {int(etc)}원")
    return drinks, etc

def save_data(data, filename='budget_data.txt'):        # 텍스트 파일에 데이터 저장
    with open(filename, 'w') as file:
        file.write(str(data))

def load_data(filename='budget_data.txt'):      # 텍스트파일에서 데이터 열람
    with open(filename, 'r') as file:
        data = eval(file.read())
    return data

def plot_exp(expenses):     # 지출 그래프 시각화
    months = list(expenses.keys())
    values = list(expenses.values())

    plt.plot(months, values, marker='o')
    plt.xlabel('Month')
    plt.ylabel('Expenses')
    plt.title('Monthly Expenses')
    plt.show()

def input_monthly_exp():        # 월별 지출 금액 입력
    month_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    
    current_month = int(input("현재 월을 1부터 12까지 숫자로 입력해 주십시오: "))
    
    monthly_exp = {}
    for i in range(current_month):
        month = month_names[i]
        expense = int(input(f"{month}월의 지출 금액: "))
        monthly_exp[month] = expense
    
    
    return monthly_exp

def main():   # 메인 함수
    print("본 프로그램은 생활비를 예산하는 프로그램입니다.")
    values = fun_input()
    rest_meeting_exp, salary_savings, living_expenses, meal_expenses, groceries, transport_cost = fun_salary(values[0], values[2], values[3], values[4])
    
    drinks, etc = fun_pocket_money(values[1], rest_meeting_exp)
    
    expense_data = {
        'Living': living,
        'sen Meals': values[2] * 25000,
        'jun Meals': values[3] * 13000,
        'Groceries': groceries,
        'Transport': transport,
        'Savings': savings,
        'Drinks': drinks,
        'Etc': etc
    }
    
    save_data(expense_data)
    loaded_data = load_data()
    
    monthly_exp = input_monthly_exp()
    plot_exp(monthly_exp)