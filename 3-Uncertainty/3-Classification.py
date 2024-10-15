from tabulate import tabulate

rules = [
    {"conditions": {"种子有果皮"}, "conclusion": "被子植物"},
    {"conditions": {"种子无果皮"}, "conclusion": "裸子植物"},
    {"conditions": {"无茎叶", "无根"}, "conclusion": "藻类植物"},
    {"conditions": {"被子植物", "有托叶"}, "conclusion": "蔷薇科"},
    {"conditions": {"被子植物", "吸引菜粉蝶"}, "conclusion": "十字花科"},
    {"conditions": {"被子植物", "十字形花冠"}, "conclusion": "十字花科"},
    {"conditions": {"被子植物", "缺水环境"}, "conclusion": "仙人掌科"},
    {"conditions": {"被子植物", "蔷薇科", "有刺"}, "conclusion": "玫瑰"},
    {"conditions": {"被子植物", "水生", "可食用", "结果实"}, "conclusion": "荷花"},
    {"conditions": {"被子植物", "仙人掌科", "喜阳", "有刺"}, "conclusion": "仙人球"},
    {"conditions": {"藻类植物", "水生", "药用"}, "conclusion": "水棉"},
    {"conditions": {"被子植物", "蔷薇科", "木本", "可食用", "结果实"}, "conclusion": "苹果树"},
    {"conditions": {"被子植物", "十字花科", "黄色花", "可食用", "结果实"}, "conclusion": "油菜"},
    {"conditions": {"藻类植物", "水生", "可食用", "有白色粉末"}, "conclusion": "海带"},
    {"conditions": {"裸子植物", "木本", "叶片针状", "结果实"}, "conclusion": "松树"},
]

all_features = [
    "种子有果皮", "种子无果皮", "无茎叶", "无根", "有托叶", "吸引菜粉蝶",
    "十字形花冠", "缺水环境", "有刺", "水生", "可食用", "结果实", "喜阳",
    "药用", "木本", "有白色粉末", "叶片针状", "黄色花",
    "被子植物", "裸子植物", "藻类植物", "蔷薇科", "十字花科", "仙人掌科"
]

plants = {"玫瑰", "荷花", "仙人球", "水棉", "苹果树", "油菜", "海带", "松树"}

def forward_reasoning(known_features, rules):
    """
    正向推理函数，基于已知特征和规则库推导新的特征。
    """
    inferred = True
    while inferred:
        inferred = False
        for rule in rules:
            # 如果规则的条件是已知特征的子集，且结论尚未得出
            if rule["conditions"].issubset(known_features) and rule["conclusion"] not in known_features:
                known_features.add(rule["conclusion"])
                inferred = True
    return known_features

def match_plants(known_features, plant_rules):
    """
    计算每个植物的匹配程度，返回匹配的植物及其匹配度。
    """
    plant_scores = {}
    for plant_rule in plant_rules:
        plant = plant_rule["conclusion"]
        conditions = plant_rule["conditions"]
        match_count = len(conditions.intersection(known_features))
        total_conditions = len(conditions)
        score = match_count / total_conditions
        plant_scores[plant] = score
    return plant_scores

def backward_reasoning(known_features, possible_plants, plant_rules):
    """
    逆向推理函数，询问用户可能的特征以提高匹配度。
    """
    for plant, score in possible_plants:
        print(f"\nIn order to determine whether it is {plant}, please answer the following features:")
        for feature in plant_rules[plant]:
            if feature not in known_features:
                answer = input(f"Is the plant feature '{feature}'? (Y/n): ")
                if answer.lower() in {"y", ""}:
                    known_features.add(feature)
        known_features = forward_reasoning(known_features, rules)
    return known_features

def main():
    # Create a mapping from serial numbers to features
    feature_mapping = {str(i + 1): feature for i, feature in enumerate(all_features)}
    total_features = len(all_features)

    while True:
        print("\nThese are the features you can choose from: ")
        
        # *** Modified Output Section Start ***
        # Create a list of lists, each inner list represents a row with up to 3 features
        table_rows = []
        row = []
        for i, feature in enumerate(all_features, start=1):
            cell = f"{i}. {feature}"
            row.append(cell)
            if i % 4 == 0:
                table_rows.append(row)
                row = []
        if row:  # Append any remaining features that don't make a full row
            table_rows.append(row)
        
        # Define headers (empty since we're numbering the features)
        headers = []
        # Print the table using tabulate
        print(tabulate(table_rows, headers=headers, tablefmt="grid", stralign="left"))
        # *** Modified Output Section End ***
        print("\n")

        # 用户输入特征序号
        user_features = set()
        user_input = input("Please enter the plant feature numbers separated by spaces: ").strip()
        
        input_numbers = user_input.split()
        invalid_numbers = []
        for num in input_numbers:
            if num in feature_mapping:
                user_features.add(feature_mapping[num])
            else:
                invalid_numbers.append(num)
        
        if invalid_numbers:
            print(f"The following numbers are invalid and will be ignored: {' '.join(invalid_numbers)}")

        # 正向推理
        known_features = forward_reasoning(user_features, rules)

        # 检查是否得出植物名称
        identified_plants = plants.intersection(known_features)

        if identified_plants:
            print("\nResult:")
            for plant in identified_plants:
                print(f"The plant may be: {plant}")
        else:
            # 计算匹配度
            plant_scores = match_plants(known_features, [rule for rule in rules if rule["conclusion"] in plants])

            # 排序植物按匹配度降序
            sorted_plants = sorted(plant_scores.items(), key=lambda x: x[1], reverse=True)
            
            # 过滤出匹配度大于0的植物
            possible_plants = [(plant, score) for plant, score in sorted_plants if score > 0]

            if not possible_plants:
                print("\nSorry, the system cannot identify the plant.")
                continue

            print("\nFailed to uniquely identify the plant, possible plants and matching degree:")
            for plant, score in possible_plants:
                print(f"{plant}，matching degree: {score*100:.2f}%")
            
            # 逆向推理，询问用户更多特征
            # Pass a dictionary mapping plant to their conditions for easier access
            plant_rules_dict = {plant: [cond for cond in rule["conditions"]] for rule, plant in zip([r for r in rules if r["conclusion"] in plants], [r["conclusion"] for r in rules if r["conclusion"] in plants])}
            
            known_features = backward_reasoning(known_features, possible_plants, plant_rules_dict)

            # 再次检查是否得出植物名称
            identified_plants = plants.intersection(known_features)
            if identified_plants:
                print("\nResult:")
                for plant in identified_plants:
                    print(f"The plant may be: {plant}")
            else:
                print("\nSorry, the system cannot identify the plant.")

        continue_query = input("\nAre you going to continue the next query? (Y/n): ")
        if continue_query.lower() not in {"y", "yes", ""}:
            print("Exiting the system...")
            break
        else:
            print("\033c", end="")  # Clear the screen (works on some terminals)

if __name__ == "__main__":
    main()
