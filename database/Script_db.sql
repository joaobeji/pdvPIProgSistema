Create database db_pastelaria;
use db_pastelaria;


create table produtos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    codigo INT NOT NULL UNIQUE,
    descricao varchar(100),
    preco decimal(10, 2),
    quantidade decimal(10, 2),
    categoria varchar(50)
);

/*

CATEGORIA:
Bolos
Doces
Salgados    
Tortas
Bebidas
Pães
Lanches
Biscoitos
Produtos de confeitaria
Bebidas
Sucos
Refrigerantes
Cafés   
*/

INSERT INTO produtos (codigo, descricao, preco, quantidade, categoria) VALUES
(1, 'Bolo de Chocolate com Cobertura', 45.50, 10.00, 'Bolos'),
(2, 'Brigadeiro Gourmet Unidade', 3.50, 150.00, 'Doces'),
(3, 'Coxinha de Frango com Catupiry', 7.80, 80.00, 'Salgados'),
(4, 'Torta de Limão Merengada', 55.00, 12.00, 'Tortas'),
(5, 'Água Mineral sem Gás 500ml', 4.00, 200.00, 'Bebidas'),
(6, 'Pão Francês Fresco (unidade)', 1.50, 300.00, 'Pães'),
(7, 'Sanduíche Natural de Peito de Peru', 18.00, 40.00, 'Lanches'),
(8, 'Biscoito de Polvilho Doce 150g', 8.90, 75.00, 'Biscoitos'),
(9, 'Macaron Sortido (unidade)', 6.00, 60.00, 'Produtos de confeitaria'),
(10, 'Suco de Laranja Natural 300ml', 8.50, 90.00, 'Sucos'),
(11, 'Refrigerante Cola Lata 350ml', 6.00, 180.00, 'Refrigerantes'),
(12, 'Café Expresso Curto', 5.00, 100.00, 'Cafés'),
(13, 'Bolo de Cenoura com Brigadeiro', 48.00, 8.00, 'Bolos'),
(14, 'Beijinho de Coco Tradicional', 3.00, 120.00, 'Doces'),
(15, 'Mini Pizza de Calabresa', 9.50, 60.00, 'Salgados'),
(16, 'Torta Holandesa Cremosa', 58.00, 10.00, 'Tortas'),
(17, 'Refrigerante Guaraná Lata 350ml', 6.00, 170.00, 'Bebidas'),
(18, 'Pão de Queijo Congelado 500g', 15.00, 50.00, 'Pães'),
(19, 'Misto Quente no Pão de Forma', 12.00, 55.00, 'Lanches'),
(20, 'Biscoito Amanteigado Caseiro 200g', 12.50, 65.00, 'Biscoitos'),
(21, 'Cupcake de Baunilha com Glacê', 9.00, 45.00, 'Produtos de confeitaria'),
(22, 'Suco de Abacaxi com Hortelã 300ml', 9.00, 85.00, 'Sucos'),
(23, 'Refrigerante Limão Lata 350ml', 6.00, 160.00, 'Refrigerantes'),
(24, 'Café com Leite Grande', 7.50, 95.00, 'Cafés'),
(25, 'Bolo Red Velvet com Cream Cheese', 60.00, 7.00, 'Bolos'),
(26, 'Doce de Leite Cremoso 250g', 18.00, 30.00, 'Doces'),
(27, 'Empada de Palmito Cremosa', 8.20, 70.00, 'Salgados'),
(28, 'Torta de Morango com Chantilly', 62.00, 9.00, 'Tortas'),
(29, 'Cerveja Artesanal Lager 330ml', 15.00, 100.00, 'Bebidas'),
(30, 'Pão de Forma Integral 500g', 10.00, 40.00, 'Pães'),
(31, 'Wrap de Frango Grelhado', 22.00, 35.00, 'Lanches'),
(32, 'Biscoito Maizena Tradicional 180g', 7.50, 80.00, 'Biscoitos'),
(33, 'Mini Bolo Vulcão de Chocolate', 25.00, 20.00, 'Produtos de confeitaria'),
(34, 'Suco Detox Verde 300ml', 10.00, 70.00, 'Sucos'),
(35, 'Refrigerante Laranja Lata 350ml', 6.00, 150.00, 'Refrigerantes'),
(36, 'Cappuccino Cremoso', 8.00, 80.00, 'Cafés'),
(37, 'Bolo de Fubá com Goiabada', 40.00, 11.00, 'Bolos'),
(38, 'Pudim de Leite Condensado Individual', 10.00, 50.00, 'Doces'),
(39, 'Kibe Frito com Carne', 7.00, 90.00, 'Salgados'),
(40, 'Torta Alemã com Chocolate', 59.00, 11.00, 'Tortas'),
(41, 'Água com Gás 500ml', 4.50, 180.00, 'Bebidas'),
(42, 'Pão de Mel Recheado (unidade)', 5.00, 100.00, 'Pães'),
(43, 'X-Salada Completo', 25.00, 30.00, 'Lanches'),
(44, 'Biscoito Recheado Morango 140g', 4.50, 120.00, 'Biscoitos'),
(45, 'Doces Finos Variados (caixa com 6)', 40.00, 15.00, 'Produtos de confeitaria'),
(46, 'Suco de Maracujá Natural 300ml', 8.50, 75.00, 'Sucos'),
(47, 'Refrigerante Zero Lata 350ml', 6.00, 190.00, 'Refrigerantes'),
(48, 'Latte Macchiato', 9.00, 70.00, 'Cafés'),
(49, 'Bolo de Milho Cremoso', 42.00, 9.00, 'Bolos'),
(50, 'Mini Churros com Doce de Leite', 12.00, 60.00, 'Doces');

ALTER TABLE produtos
ADD COLUMN url_imagem VARCHAR(255);

create table usuario (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    codigo INT NOT NULL UNIQUE,
    usuario varchar(50),
    nome varchar(50),
    senha varchar(50)
);


-- Tabelas para vendas e itens de venda
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATETIME,
    total DECIMAL(10,2)
);

CREATE TABLE itens_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT,
    codigo_produto VARCHAR(20),
    nome_produto VARCHAR(100),
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    total DECIMAL(10,2),
    FOREIGN KEY (venda_id) REFERENCES vendas(id)
);

CREATE TABLE vendas_canceladas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATETIME NOT NULL,
    motivo VARCHAR(255),
    operador VARCHAR(100)
);
