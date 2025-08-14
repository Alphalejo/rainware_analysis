-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS sales_predictions (
    id SERIAL PRIMARY KEY,
    date DATE,
    product_id INT,
    sales INT,
    price DOUBLE PRECISION,
    category VARCHAR(50),
    temperature DOUBLE PRECISION,
    sales_prediction DOUBLE PRECISION
);



-- Error promedio por categoría
SELECT
    category,
    AVG(ABS(sales - sales_prediction)) AS avg_error
FROM sales_predictions
GROUP BY category;
