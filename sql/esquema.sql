-- ============================================================
-- ESQUEMA DE BASE DE DATOS
-- SISTEMA DE MONITOREO DE BIODIVERSIDAD Y ARACNOFAUNA
-- ============================================================

CREATE DATABASE IF NOT EXISTS biodiversidad;

USE biodiversidad;

-- ============================================================
-- TABLA USUARIOS
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (

    id INT NOT NULL AUTO_INCREMENT,

    usuario VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    PRIMARY KEY (id)

);
