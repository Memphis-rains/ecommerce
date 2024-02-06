import psycopg2
from faker import Faker

db_params = {
    'host': 'localhost',
    'dbname': 'zdb',
    'user': 'postgres',
    'password': 'sapan',
    'port': '5432',
}

fake = Faker()

def generate_user_records(num_records):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for _ in range(num_records):
        fake_name = fake.name()
        fake_phone = fake.random_number(10)
        fake_email = fake.email()
        fake_password = fake.password()

        insert_query = '''
            INSERT INTO users_customer (user_name, user_phone, user_email, user_password)
            VALUES (%s, %s, %s, %s);
        '''

        cursor.execute(insert_query, (fake_name, fake_phone, fake_email, fake_password))

    conn.commit()
    cursor.close()
    conn.close()

def generate_seller_records(num_records):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    for i in range(num_records):
        fake_name = fake.name()
        fake_bname = (fake.name() + "'s Shop" + str(i))[:30]

        fake_GSTIN = "GSTIN" + str(fake.random_number(8))
        fake_address = fake.address()
        fake_email = fake.email()
        fake_phno = fake.random_number(8)

        # Check if a record with the same business name already exists
        check_query = '''
            SELECT COUNT(*) FROM sellers_seller WHERE business_name = %s;
        '''
        cursor.execute(check_query, (fake_bname,))
        count = cursor.fetchone()[0]

        if count == 0:
            # If no record exists, insert the new record
            insert_query = '''
                INSERT INTO sellers_seller (seller_name, business_name, gstin_number, seller_shop_address, seller_email, seller_phone, seller_complaints)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''
            cursor.execute(insert_query, (fake_name, fake_bname, fake_GSTIN, fake_address, fake_email, fake_phno, 0))

    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    
    num_records_to_generate = 1000
    #generate_user_records(num_records_to_generate)
    generate_seller_records(num_records_to_generate)
    print(f'Successfully generated and saved {num_records_to_generate} fake records.')

