import pandas as pd
import math
import numpy
from connectors.postgree import PostGreConnector
from constants import abreviacao, pontuacao, descricao

from models.Players import Player
from models.Matches import Match
from models.Positions import Position
from models.Scouts import Scout
from models.Skills import Skill
from models.Teams import Team


class Pandas2DB():

    def __init__(self):
        self.db_con = PostGreConnector()

    def createtables(self):
        self.db_con.CreateAllTables()


    def InsertPlayer(self, df):
        DB_list = Pandas2DB.Df2Db_Player(df)
        # self.db_con.InsertElement(DB_list[0])
        self.db_con.InsertList(DB_list)

    def InsertMatch(self, df):
        DB_list = Pandas2DB.Df2Db_Match(df)
        self.db_con.InsertList(DB_list)

    def InsertPosition(self, df):
        DB_list = Pandas2DB.Df2Db_Position(df)
        self.db_con.InsertList(DB_list)

    def InsertScout(self, df):
        DB_list = Pandas2DB.Df2Db_Scout(df)
        # self.db_con.InsertList(DB_list)
        self.db_con.InsertListManual(DB_list)

    def InsertSkill(self):
        DB_list = Pandas2DB.Df2Db_Skill()
        self.db_con.InsertList(DB_list)

    def InsertTeam(self, df):
        DB_list = Pandas2DB.Df2Db_Team(df)
        self.db_con.InsertList(DB_list)

    @staticmethod
    def Df2Db_Player(df):
        DB_list = []
        for index, row in df.iterrows():
            if not math.isnan(row['Clube']):
                jogador = Player(id = row['ID'], name = row['Apelido'], team_id = int(row['Clube']), position_id = int(row['Posicao']),
                            year = row['Year'])
                DB_list.append(jogador)
        return DB_list

    @staticmethod
    def Df2Db_Match(df):
        DB_list = []
        for index, row in df.iterrows():
            partida = Match(id = row['ID'] - 179872, home_team_id = int(row['Casa']), visiting_team_id = int(row['Visitante']), result = row['Resultado'],
                       home_score = int(row['PlacarCasa']), visiting_score= int(row['PlacarVisitante']),
                        match_week = row['Rodada'], year = row['Year'])
            DB_list.append(partida)
        return DB_list

    @staticmethod
    def Df2Db_Position(df):
        DB_list = []
        for index, row in df.iterrows():
            posicao = Position(id = row['ID'], name = row['Nome'], nickname = row['Abreviacao'])
            DB_list.append(posicao)
        return DB_list

    @staticmethod
    def Df2Db_Scout(df):
        DB_list = []
        for index, row in df.iterrows():
            Play_list = []
            for sigla in abreviacao:
                Play_list.append(int(row[sigla]))
            if not math.isnan(row['Clube']):
                scouts = Scout(id= int(index), player_id= int(row['Atleta']),
                          team_id= row['Clube'], has_played= bool(row['Participou']), points= float(row['Pontos']),
                          average_points= float(row['PontosMedia']), price= float(row['Preco']),
                          delta_price= float(row['PrecoVariacao']), plays= 1,
                          year= int(row['Year']))
                DB_list.append(scouts)
        return DB_list

    @staticmethod
    def Df2Db_Skill():
        DB_list = []
        for index in range(0, len(abreviacao)):
            skill = Skill(id = index, name= descricao[index], nickname= abreviacao[index], points= pontuacao[index])
            DB_list.append(skill)
        return DB_list

    @staticmethod
    def Df2Db_Team(df):
        DB_list = []
        for index, row in df.iterrows():
            times = Team(id= row['ID'], name= row['Slug'], nickname= row['Abreviacao'], year= row['Year'])
            DB_list.append(times)
        return DB_list


