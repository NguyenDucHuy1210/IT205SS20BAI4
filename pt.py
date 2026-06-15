import logging
import os

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="data/roster_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    encoding="utf-8"
)

roster = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched"
    }
]

def display_roster(roster_list):
    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    if not roster_list:
        print("Đội hình hiện đang trống.")
        return
    
    print(f"{'ID':<8}|{'Tên tuyển thủ':<25}|{'Vị trí':<15}|{'Lương':<12}|Trạng thái")
    print("-" * 80)
    
    for player in roster_list:
        try:
            p_id = player.get("player_id")
            name = player.get("name")
            role = player.get("role")
            salary = player.get("salary")
            status = player.get("status")
            
            if None in (p_id, name, role, salary, status):
                raise KeyError("Thiếu thuộc tính bắt buộc của tuyển thủ.")
                
            if status == "Benched":
                name += " [DỰ BỊ]"
                
            print(
                f"{p_id:<8}|"
                f"{name:<25}|"
                f"{role:<15}|"
                f"{salary:<12,.1f}|"
                f"{status}"
            )
        except KeyError as e:
            print(f"[LỖI DATA] Không thể hiển thị một tuyển thủ do thiếu thông tin: {e}")
            logging.error(f"KeyError in display_roster: {e}")
            
    logging.info("Coach viewed the team roster.")

def sign_player(roster_list):
    print("\n--- CHIÊU MỘ TUYỂN THỦ MỚI ---")
    player_id = input("Nhập mã tuyển thủ: ").upper()
    
    for player in roster_list:
        if player.get("player_id") == player_id:
            print(f"Lỗi: Mã tuyển thủ {player_id} đã tồn tại.")
            logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
            return
            
    name = input("Nhập tên tuyển thủ: ").title()
    role = input("Nhập vị trí thi đấu: ").title()
    
    while True:
        try:
            salary = float(input("Nhập mức lương hàng tháng: "))
            if salary <= 0:
                print("Lương phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Lương phải là số. Vui lòng nhập lại.")
            logging.warning("Failed to sign player - Invalid salary input")
            
    roster_list.append({
        "player_id": player_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    })
    print(f"Thành công: Đã chiêu mộ tuyển thủ {name}.")
    logging.info(f"Signed new player {name} with salary {salary}")

def update_player_status(roster_list):
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")
    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").upper()
    
    for player in roster_list:
        if player.get("player_id") == player_id:
            print(f"\nTuyển thủ: {player.get('name')}")
            print(f"Vị trí: {player.get('role')}")
            print(f"Lương hiện tại: {player.get('salary')}")
            print(f"Trạng thái hiện tại: {player.get('status')}")
            
            print("\n1. Cập nhật lương")
            print("2. Cập nhật trạng thái")
            try:
                choice = int(input("Chọn: "))
            except ValueError:
                print("Lựa chọn không hợp lệ.")
                return
                
            match choice:
                case 1:
                    while True:
                        try:
                            new_salary = float(input("Nhập mức lương mới: "))
                            if new_salary <= 0:
                                print("Lương phải là số dương.")
                                continue
                            old_salary = player["salary"]
                            player["salary"] = new_salary
                            print("Cập nhật thành công.")
                            logging.info(f"Updated player {player_id} salary from {old_salary} to {new_salary}")
                            return
                        except ValueError:
                            print("Lương phải là số.")
                case 2:
                    print("1. Active")
                    print("2. Benched")
                    try:
                        status_choice = int(input("Chọn: "))
                    except ValueError:
                        print("Lựa chọn không hợp lệ.")
                        return
                    old_status = player["status"]
                    match status_choice:
                        case 1:
                            player["status"] = "Active"
                        case 2:
                            player["status"] = "Benched"
                        case _:
                            print("Lựa chọn không hợp lệ.")
                            return
                    print("Cập nhật thành công.")
                    logging.info(f"Updated player {player_id} status from {old_status} to {player['status']}")
                    return
                case _:
                    print("Lựa chọn không hợp lệ.")
                    return
                    
    print(f"Không tìm thấy tuyển thủ mang mã {player_id}.")
    logging.warning(f"Failed to update player - Player ID {player_id} not found")

def generate_payroll_report(roster_list):
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return
        
    total = 0
    print(f"{'ID':<8}|{'Tên tuyển thủ':<15}|{'Trạng thái':<10}|{'Lương gốc':<12}|Lương thực nhận")
    print("-" * 80)
    
    try:
        for player in roster_list:
            if "salary" not in player or "status" not in player:
                raise KeyError("Thiếu trường dữ liệu tính lương.")
                
            salary = player["salary"]
            if player["status"] == "Active":
                receive = salary
            else:
                receive = salary * 0.5
            total += receive
            
            print(
                f"{player.get('player_id', 'N/A'):<8}|"
                f"{player.get('name', 'N/A'):<15}|"
                f"{player.get('status', 'N/A'):<10}|"
                f"{salary:<12,.1f}|"
                f"{receive:,.1f}"
            )
        print("-" * 80)
        print(f"Tổng quỹ lương hàng tháng: {total:,.1f}")
        logging.info(f"Generated monthly payroll report. Total: {total}")
    except KeyError as e:
        print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
        print("-" * 80)
        print("Tổng quỹ lương hàng tháng: 0.0")
        logging.error(f"Missing key while generating payroll report: {e}")

def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====")
        print("1. Xem đội hình thi đấu hiện tại")
        print("2. Chiêu mộ tuyển thủ mới")
        print("3. Cập nhật lương & Trạng thái thi đấu")
        print("4. Báo cáo quỹ lương hàng tháng")
        print("5. Thoát hệ thống")
        try:
            choice = int(input("Chọn chức năng (1-5): "))
        except ValueError:
            print("Lựa chọn không hợp lệ.")
            continue
            
        match choice:
            case 1:
                display_roster(roster)
            case 2:
                sign_player(roster)
            case 3:
                update_player_status(roster)
            case 4:
                generate_payroll_report(roster)
            case 5:
                logging.info("System shutdown.")
                print("Đã thoát hệ thống.")
                break
            case _:
                print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()