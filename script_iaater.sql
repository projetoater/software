create database iaater;
use iaater;

create table perfis (
	idperfil int not null auto_increment,
    perfil varchar(50) not null,
    bio varchar(255) not null,
    constraint pk_perfis_idperfil primary key(idperfil)
);

create index idx_perfis_bio on perfis(bio);

create table palavras(
	idpalavra int not null auto_increment, 
    palavra varchar(255) not null,
    constraint pk_palavras_palavra primary key (idpalavra)
);

create index idx_palavras_palavra on palavras(palavra);

create table palavra_localizacao (
	idpalavra_localizacao int not null auto_increment,
    idperfil int not null,
    idpalavra int not null,
    localizacao int,
    constraint pk_idpalavra_localizacao primary key (idpalavra_localizacao),
    constraint fk_palavra_localizacao_idperfil foreign key (idperfil) references perfis(idperfil),
    constraint fk_palavra_localizacao_idpalavra foreign key (idpalavra) references palavras(idpalavra)
);

create index idx_palavra_localizacao_idpalavra on palavra_localizacao (idpalavra);

alter database iaater character set = utf8mb4 collate = utf8mb4_unicode_ci;
alter table palavras convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table palavras modify column palavra varchar(255) character set utf8mb4 collate utf8mb4_unicode_ci;