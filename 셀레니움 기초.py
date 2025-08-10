from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def connect_to_srt():
    """SRT 웹사이트에 접속하는 함수"""
    
    # Chrome 옵션 설정
    chrome_options = Options()
    # 헤드리스 모드를 원하지 않으면 아래 줄을 주석처리하세요
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # User-Agent 설정으로 봇 탐지 방지
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # WebDriver 초기화
        driver = webdriver.Chrome(options=chrome_options)
        
        # 봇 탐지 방지를 위한 스크립트 실행
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("SRT 웹사이트에 접속 중...")
        
        # SRT 웹사이트 접속
        driver.get("https://etk.srail.kr/main.do")
        
        # 페이지 로딩 대기
        wait = WebDriverWait(driver, 10)
        
        # 페이지 제목이 로드될 때까지 대기
        wait.until(lambda driver: driver.title != "")
        
        print(f"접속 성공! 페이지 제목: {driver.title}")
        print(f"현재 URL: {driver.current_url}")
        
        # 잠시 대기 (페이지 완전 로딩)
        time.sleep(3)
        
        # 주요 요소들이 로드되었는지 확인
        try:
            # 출발지 선택 요소 확인
            departure_element = wait.until(
                EC.presence_of_element_located((By.ID, "dptRsStnCd"))
            )
            print("출발지 선택 요소 발견됨")
            
            # 도착지 선택 요소 확인  
            arrival_element = wait.until(
                EC.presence_of_element_located((By.ID, "arvRsStnCd"))
            )
            print("도착지 선택 요소 발견됨")
            
            print("메인 페이지 요소들이 정상적으로 로드되었습니다.")
            
        except Exception as e:
            print(f"일부 요소 로딩 실패: {e}")
        
        # 지정된 CSS 셀렉터 클릭
        try:
            # CSS 셀렉터로 요소 찾기
            target_selector = "#wrap > div.header.header-e > div.global.clear > div > a:nth-child(2)"
            target_element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, target_selector))
            )
            
            print(f"타겟 요소 발견: {target_element.text if target_element.text else '텍스트 없음'}")
            
            # 요소 클릭
            driver.execute_script("arguments[0].click();", target_element)
            print("CSS 셀렉터 요소 클릭 완료")
            
            # 클릭 후 잠시 대기
            time.sleep(2)
            
            print(f"클릭 후 현재 URL: {driver.current_url}")
            
            # "tt" 텍스트 입력
            try:
                # 활성화된 입력 필드 찾기 (일반적인 입력 필드들)
                input_selectors = [
                    "input[type='text']",
                    "input[type='email']", 
                    "input[type='search']",
                    "input:not([type='hidden']):not([type='submit']):not([type='button'])",
                    "textarea"
                ]
                
                input_element = None
                for selector in input_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        # 보이는 요소 중 첫 번째 찾기
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                input_element = element
                                break
                        if input_element:
                            break
                    except:
                        continue
                
                if input_element:
                    # 입력 필드를 찾은 경우
                    input_element.clear()  # 기존 내용 지우기
                    input_element.send_keys("1234")
                    print("입력 필드에 '회원번호' 입력 완료")
                else:
                    print("입력 필드를 찾을 수 없습니다")
            except Exception as e:
                print(f"텍스트 입력 실패: {e}")
                # 최후의 방법: JavaScript로 입력 시도
                try:
                    driver.execute_script("document.activeElement.value = 'tt';")
                    print("JavaScript로 'tt' 입력 완료")
                except Exception as e2:
                    print(f"JavaScript 입력도 실패: {e2}")
            
            # 입력 후 잠시 대기
            time.sleep(1)
            
            # 출발지 선택 기능 추가
            print("출발지 선택을 시도합니다...")
            
            # 출발지 선택 버튼 클릭 (드롭다운 열기)
            departure_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "dptRsStnCd"))
            )
            departure_btn.click()
            print("출발지 드롭다운 열기 완료")
            
            # 잠시 대기 (드롭다운 로딩)
            time.sleep(1)
            
            # 출발지 옵션들 찾기
            departure_options = driver.find_elements(By.CSS_SELECTOR, "#dptRsStnCd option")
            
            if departure_options:
                print("사용 가능한 출발지 목록:")
                for i, option in enumerate(departure_options[:10]):  # 처음 10개만 표시
                    if option.text.strip():
                        print(f"  {i}: {option.text}")
                
                # 예시: "수서" 선택 (첫 번째 실제 역)
                target_departure = "수서"
                selected = False
                
                for option in departure_options:
                    if target_departure in option.text:
                        option.click()
                        print(f"출발지 '{target_departure}' 선택 완료")
                        selected = True
                        break
                
                if not selected:
                    # 수서가 없으면 첫 번째 유효한 옵션 선택
                    for option in departure_options:
                        if option.text.strip() and option.text != "선택":
                            option.click()
                            print(f"출발지 '{option.text}' 선택 완료")
                            break
                            
            else:
                print("출발지 옵션을 찾을 수 없습니다")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"출발지 선택 실패: {e}")
            
            # 대안 방법: JavaScript로 직접 값 설정
            try:
                # Select 요소에 직접 값 설정
                driver.execute_script("""
                    var selectElement = document.getElementById('dptRsStnCd');
                    if (selectElement && selectElement.options.length > 1) {
                        selectElement.selectedIndex = 1; // 첫 번째 실제 옵션 선택
                        selectElement.dispatchEvent(new Event('change'));
                        console.log('출발지 JavaScript로 선택 완료');
                    }
                """)
                print("JavaScript로 출발지 선택 완료")
            except Exception as e2:
                print(f"JavaScript 출발지 선택도 실패: {e2}")
            
        except Exception as e:
            print(f"CSS 셀렉터 클릭 실패: {e}")
            # 대안: 직접 CSS 셀렉터로 재시도
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, target_selector)
                if elements:
                    driver.execute_script("arguments[0].click();", elements[0])
                    print("대안 방법으로 클릭 성공")
                else:
                    print("해당 셀렉터의 요소를 찾을 수 없습니다")
            except Exception as e2:
                print(f"대안 클릭도 실패: {e2}")
        
        # 스크린샷 저장 (선택사항)
        try:
            driver.save_screenshot("/Users/polljun/project-newlife/srt_screenshot.png")
            print("스크린샷이 저장되었습니다: srt_screenshot.png")
        except Exception as e:
            print(f"스크린샷 저장 실패: {e}")
        
        return driver
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def main():
    """메인 실행 함수"""
    driver = connect_to_srt()
    
    if driver:
        try:
            # 여기에 추가 작업을 수행할 수 있습니다
            # 예: 승차권 조회, 예약 등
            
            input("엔터를 눌러 브라우저를 종료하세요...")
            
        finally:
            # 브라우저 종료
            driver.quit()
            print("브라우저가 종료되었습니다.")
    else:
        print("웹사이트 접속에 실패했습니다.")

if __name__ == "__main__":
    main()
