import os
import pickle

import boto3
import numpy as np
import pandas
import s3creds


def downloadFromS3(s3_fileName):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=s3creds.aws_access_key_id,
        aws_secret_access_key=s3creds.aws_secret_access_key
    )
    return s3.get_object(Bucket="botrecord", Key="Tabela")


def getTabela():
    response = downloadFromS3("Tabela")
    body = response["Body"].read()
    return pickle.loads(body)


def reduceTableDetails(tabela):
    """
        Reduz os detalhes da tabela final. Limita-se a imprimir tabela com ranking equipa e pontos.
    """
    tabelaCompact = tabela[["Equipa", "Pontos"]]
    tabelaSorted = tabelaCompact.sort_values(["Pontos"], ascending=False)
    tabelaSorted = tabelaSorted.reset_index(drop=True)
    tabelaSorted.index = np.arange(1, len(tabelaSorted) + 1)
    return tabelaSorted.to_string()