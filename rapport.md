# S103 Report
By Galaad Martineaux, Mattew Kerlidou, and Matthieu Da Cruz.
## Summary
1. [Installing Raspberry Pi OS](#heading1)
1. [Add the users required](#heading2)
1. [Install MariaDB, and configure it.](#heading3)
1. [Install ssh](#heading4)
1. [Add the required user to MariaDB](#heading5)
1. [Add the required tables to the database.](#heading6)
1. [Fill the tables with the data.](#heading7)
1. [What went wrong](#heading8)

<a id="heading1"></a>
## 1. Installing Raspberry Pi Os
We began by writing the `img.xz` file containing the operating system install wizard contained in `/Pub/S103/distro/`
to the SD card that will serve as storage for the Raspberry Pi.
After this, we simply followed the instructions.

<a id="heading2"></a>
## 2. Add the users required
As we should add the user `student` to the Raspberry Pi OS Linux install,
we used the following command:
```sh
adduser student
```

<a id="heading3"></a>
## 3. Install MariaDB, and configure it.
First off, installing MariaDB.
We executed the following command to download it from the distant repositories:
```sh
sudo apt-get install mariadb-server
```

Then, we needed to both start MariaDB and make sure it starts on startup:
```sh
sudo systemctl enable mariadb #Make it so MariaDB starts on startup.
sudo systemctl start mariadb #Start MariaDB
```

Finally, we'll need to configure MariaDB and the mysql installation using the two following commands.
```sh
sudo mysql_secure_installation
sudo nano /etc/mysql/mariadb.conf.d/50-mysql-clients.cnf
```
The second command, pops the `nano` editor which will allow to edit the write-protected configuration of
MariaDB.
We needed to replace `bind-address = 127.0.0.1` by `bind-address = 0.0.0.0`.

<a id="heading4"></a>
## 4. Install ssh
`ssh` will allow remote connection to the Raspberry Pi, which is why we need it.
We will not need to download it or install it as its a pre-installed binary on this
distribution.
To start it and make it start on startup, we used the following commands:
```sh
sudo systemctl enable ssh #Make ssh start on startup
sudo systemctl start ssh #Start ssh
```

<a id="heading5"></a>
## 5. Add the required user to MariaDB
We had to create the user `prof`, with password `pwdprof` for the database.
```sql
CREATE USER prof@s103 IDENTIFIED BY 'pwdprof';
```

Then, we needed to grant them some privileges. We decided to give them all privileges:
```sql
GRANT ALL PRIVILEGES ON *.* TO 'prof'@'%';
```

<a id="heading6"></a>
## 6. Add the required tables to the database.
We needed to create the following and database, and fill them with the following data:

**ACTICAMPING**
| NumCamping		| NumActivite	   | PrixActivite |
| :---------------  |:---------------:  | -----:|
| 1				 | 101			   |  20.50 |
| 1				 | 102			   |   15.75 |
| 2				 | 101			   |	18.00 |

**ACTIVITE**
| NumActivite		| NumActivite	   | TypeActivite |
| :---------------  |:---------------:  | -----:|
| 101				 | Randonnée			   |  Plein air |
| 102				 | Escalade			   |   Aventure |
| 103				 | Yoga			   |	Bien-être |


**CAMPING**
| NumCamping		| NomCamping	   | AddrCamping | TelCamping | DateOuv | DateFerm | NbEtoiles | QualiteFrance
| :---------------- |:----------------:|:----------:|:----------:|:-------:|:---------:|:---------:|-------------:
| 1					| Le Paradis| 123 Rue de la Forêt| 01 23 45 67 89| 2023-05-01| 2023-10-31| 4 | Excellente
| 2					| Belle Nature| 456 Avenue des Montagnes| 98 76 54 32 10| 2023-06-15| 2023-09-30| 3 | Bonne
Creation of ACTICAMPING Table:
```sql
CREATE TABLE ACTICAMPING (NumCamping INTEGER NOT NULL
	NumActivite INTEGER NOT NULL,			--Integer
	PrixActivite REAL NOT NULL,
	PRIMARY KEY(NumActivite, NumCamping)	--Real
);
```

Creation of ACTIVITE table:
```sql
CREATE TABLE ACTIVITE (
	NumActivite INTEGER NOT NULL,		--Integer
	NomActivite VARCHAR(100) NOT NULL,	--Text between 0 to 100 characters
	TypeActivite VARCHAR(50) NOT NULL,	--Text from 0 to 50 characters
	PRIMARY KEY(NumActivite)			--Primary Key
);
```

Creation of CAMPING Table:
```sql
CREATE TABLE CAMPING (
    NumCamping INTEGER NOT NULL AUTO_INCREMENT,	--Integer that increments itself with each insertion
    NomCamping VARCHAR(50) NOT NULL,			--Text from 0 to 50 characters
    AddrCamping VARCHAR(1024) NOT NULL,			--Text between 0 à 1024 characters
    TelCamping VARCHAR(50) NOT NULL,			--Text from 0 to 50 characters
    DateOuv DATE NOT NULL,						--Date
    DateFerm DATE NOT NULL,						--Date
    NbEtoiles INTEGER NOT NULL,					--Integer
    QualiteFrance VARCHAR(50) NOT NULL,			--Text from 0 to 50 characters
    PRIMARY KEY(NumCamping)						--Primary Key
);
);
```

<a id="heading7"></a>
## 7. Fill the tables with the data
Insertion into the ACTICAMPING table:
```sql

--Line 1
INSERT INTO ACTICAMPING (NumCamping, NumActivite, PrixActivite)
VALUES ( 1, 101, 20.50);

--Line 2
INSERT INTO ACTICAMPING (NumCamping, NumActivite, PrixActivite)
VALUES (1, 102, 15.75);

--Line 3
INSERT INTO ACTICAMPING (NumCamping, NumActivite, PrixActivite)
VALUES (2, 101, 18.00);
```

Insertion into the ACTIVITE table:
```sql

--Line 1
INSERT INTO ACTIVITE (NumActivite, NomActivite, TypeActivite)
VALUES (101, "Randonnée pédestre", "Plein air");

--Line 2
INSERT INTO ACTIVITE (NumActivite, NomActivite, TypeActivite)
VALUES (102, "Escalade", "Aventure");

--Line 3
INSERT INTO ACTIVITE (NumActivite, NomActivite, TypeActivite)
VALUES (103, "Yoga", "Bien-être");
```

Insertion into the CAMPING table:
```sql
--Line 1
INSERT INTO CAMPING 
(
    NomCamping,
    AddrCamping,
    TelCamping,
    DateOuv,
    DateFerm,
    NbEtoiles,
    QualiteFrance
)
VALUES
(
    "Le Paradis",
    "123 Rue de la Forêt",
    "01 23 45 67 89",
    "2023-05-01",
    "2023-10-31",
    4,
    "Excellente"
);

--Line 2
INSERT INTO CAMPING 
(
    NomCamping,
    AddrCamping,
    TelCamping,
    DateOuv,
    DateFerm,
    NbEtoiles,
    QualiteFrance
)
VALUES
(
    "Belle Nature",
    "456 Avenue des Montagnes",
    "98 76 54 32 10",
    "2023-06-15",
    "2023-09-30",
    3,
    "Bonne"
);
```

<a id="heading8"></a>
## 8. What went wrong
Time updates quite a while after booting up.