
CREATE TABLE IF NOT EXISTS menu (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    available BOOLEAN DEFAULT true,
    description TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit VARCHAR(20),
    current_stock DECIMAL(10,3),
    min_stock DECIMAL(10,3),
    supplier VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(50) DEFAULT 'Новый',
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    total DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    menu_item_id INTEGER REFERENCES menu(id),
    quantity INTEGER DEFAULT 1,
    price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    menu_item_id INTEGER REFERENCES menu(id),
    inventory_id INTEGER REFERENCES inventory(id),
    quantity_required DECIMAL(10,3)
);

-- Тестовые данные
INSERT INTO menu (name, category, price, available, description) VALUES
('Стейк Рибай', 'Горячие блюда', 1200.00, true, 'Стейк с картофелем'),
('Цезарь с курицей', 'Салаты', 450.00, true, 'Салат Цезарь с куриной грудкой'),
('Томатный суп', 'Супы', 350.00, true, 'Томатный суп с базиликом'),
('Тирамису', 'Десерты', 400.00, false, 'Классический тирамису'),
('Кофе латте', 'Напитки', 250.00, true, 'Кофе латте 300 мл'),
('Бургер', 'Горячие блюда', 600.00, true, 'Бургер с говядиной')
ON CONFLICT DO NOTHING;

INSERT INTO inventory (name, category, unit, current_stock, min_stock, supplier) VALUES
('Говядина', 'Мясо', 'кг', 15.5, 5.0, 'Мясной двор'),
('Куриное филе', 'Мясо', 'кг', 8.2, 3.0, 'Птицефабрика'),
('Помидоры', 'Овощи', 'кг', 12.0, 4.0, 'Овощная база'),
('Сыр пармезан', 'Молочные', 'кг', 2.5, 1.0, 'Сыроварня'),
('Кофе зерновой', 'Бакалея', 'кг', 5.0, 2.0, 'Кофейная компания'),
('Салат Айсберг', 'Овощи', 'кг', 3.2, 2.0, 'Овощная база')
ON CONFLICT DO NOTHING;

INSERT INTO recipes (menu_item_id, inventory_id, quantity_required) VALUES
(1, 1, 0.3),  -- Стейк: 300г говядины
(2, 2, 0.2),  -- Цезарь: 200г курицы
(2, 4, 0.05), -- Цезарь: 50г пармезана
(5, 5, 0.02)  -- Кофе: 20г зерен
ON CONFLICT DO NOTHING;