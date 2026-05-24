-- [실습 1] : 데이터베이스 만들기
-- kickboard 테이블을 정의하세요.
CREATE TABLE kickboard(
    member_id VARCHAR(16),
    member_name VARCHAR(16),
    kickboard_id VARCHAR(16),
    kickboard_brand VARCHAR(16),
    rental_location VARCHAR(32),
    rental_date DATETIME,
    distance INT,
    price INT
);
-- 데이터베이스에 정의된 테이블 목록을 출력하세요.
SHOW TABLES;

-- kickboard 테이블의 구조를 출력하세요.
DESC kickboard;

-- [실습 2] : 데이터 삽입하고 출력하기
-- DESC 명령어를 통해 정의된 kickboard 테이블을 확인할 수 있습니다.
DESC kickboard;

-- 2개의 데이터를 삽입하세요.
INSERT INTO kickboard(member_id, member_name, kickboard_id, kickboard_brand, rental_location, rental_date, distance, price)
VALUES ('kmax6','김민준','7YWC','boardkick','서울시 관악구 신림동','2020-05-14 12:01:55',354, 4700);

INSERT INTO kickboard(member_id, member_name, kickboard_id, kickboard_brand, rental_location, rental_date, distance, price)
VALUES ('flykite','이서연','JXAN','willgo','서울시 동작구 대방동','2020-11-12 19:30:00',560, 7200);

-- kickboard 테이블의 데이터를 출력하세요.
SELECT * FROM kickboard

-- [실습 3] : 테이블 수정하기

-- DESC 명령어를 통해 정의된 kickboards 테이블을 확인할 수 있습니다.
DESC kickboards;

-- kickboards 테이블에 member_birthday 컬럼을 추가하세요.
ALTER TABLE kickboards ADD COLUMN member_birthday DATE NULL;

-- rental_date 속성의 데이터 타입을 TIME으로 수정하세요
ALTER TABLE kickboards MODIFY COLUMN rental_date TIME NULL;

-- member_id와 kickboard_id 컬럼의 제약 조건을 NOT NULL로 수정하세요.
ALTER TABLE kickboards MODIFY COLUMN member_id VARCHAR(16) NOT NULL;
-- ALTER TABLE kickboards MODIFY COLUMN kickboard_id VARCHAR(16) NOT NULL;

-- kickboard_id와 kickboard_brand 컬럼의 이름을 변경하세요.
ALTER TABLE kickboards CHANGE COLUMN kickboard_id id VARCHAR(16) NOT NULL;
ALTER TABLE kickboards CHANGE COLUMN kickboard_brand brand VARCHAR(16) NULL;

-- distance 컬럼을 삭제하세요.
ALTER TABLE kickboards DROP COLUMN distance;

-- kickboards 테이블의 이름을 kickboard로 수정하세요.
ALTER TABLE kickboards RENAME kickboard;

-- 수정된 kickboard 테이블의 구조를 확인해봅니다. 제출 시 아래 주석을 해제하세요.
DESC kickboard;

-- [실습 4] : 테이블 삭제하기
-- kickboard 테이블을 삭제하세요.
DROP TABLE kickboard;

-- kickboard 테이블이 삭제되었는지 확인해보세요. 아래 코드는 수정하면 안됩니다.
SHOW TABLES;