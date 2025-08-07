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

create table usuario (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    codigo INT NOT NULL UNIQUE,
    usuario varchar(50),
    nome varchar(50),
    senha varchar(50)
);