INSERT INTO employees (full_name, role, department, active) VALUES
  ('Alicia Gomez', 'HR Manager', 'People', TRUE),
  ('Mason Lee', 'Warehouse Lead', 'Operations', TRUE),
  ('Daniel Park', 'Account Executive', 'Sales', FALSE);

INSERT INTO inventory (sku, item_name, quantity, unit_cost) VALUES
  ('LAP-13-001', 'Laptop 13-inch', 24, 500),
  ('MOU-WLS-009', 'Wireless Mouse', 180, 19.99),
  ('MON-27-020', 'Monitor 27-inch', 52, 210.00);

INSERT INTO orders (order_number, customer_name, total_amount, status) VALUES
  ('SO-1001', 'Northwind Cafe', 1250.50, 'SHIPPED'),
  ('SO-1002', 'Blue Harbor', 349.00, 'PENDING'),
  ('SO-1003', 'Nova Retail', 2100.00, 'DELIVERED');
