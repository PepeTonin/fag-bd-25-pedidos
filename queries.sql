create database bd_pedidos_2025;

create table clientes (
  id int auto_increment primary key,
  nome varchar(255) not null,
  email varchar(255) not null unique,
  senha varchar(255) not null
  criado_em datetime not null default current_timestamp
  atualizado_em datetime not null default current_timestamp on update current_timestamp
);

create table produtos (
  id int auto_increment primary key,
  nome varchar(255) not null,
  descricao varchar(255) not null,
  preco decimal(10, 2) not null
  criado_em datetime not null default current_timestamp
  atualizado_em datetime not null default current_timestamp on update current_timestamp
);

create table pedidos (
  id int auto_increment primary key,
  cliente_id int not null,
  produto_id int not null,
  quantidade_produto int not null,
  foreign key (cliente_id) references clientes(id),
  foreign key (produto_id) references produtos(id)
  criado_em datetime not null default current_timestamp
);