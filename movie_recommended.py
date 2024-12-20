import pandas as pd

def basic_analysis(df):
    print("데이터 정보:")
    df.info()
    print("\n데이터 통계:")
    print(df.describe(include='all'))


def count_statistics(df):
    """
    영화 개수, 배급자 수, 감독 수, 출연진 수, 장르 수 출력
    """
    print(f"영화 개수: {df.shape[0]}")
    print(f"배급사 수: {df['배급사'].nunique()}")
    print(f"감독 수: {df['감독'].nunique()}")
    print(f"출연진 수: {df['출연진'].nunique()}")
    print(f"장르 수: {df['장르'].nunique()}")


def analyze_duplicates(df):
    """
    감독과 출연진 분리 및 중복 분석
    """
    # 감독 리스트 분리 및 중복 분석
    df['감독_리스트'] = df['감독'].str.split(', ')
    exploded_directors = df.explode('감독_리스트')
    directors_counts = exploded_directors['감독_리스트'].value_counts()

    print("\n감독별 영화 개수:")
    print(directors_counts)

    # 출연진 리스트 분리 및 중복 분석
    df['출연진_리스트'] = df['출연진'].str.split(', ')
    exploded_actors = df.explode('출연진_리스트')
    actors_counts = exploded_actors['출연진_리스트'].value_counts()

    print("\n출연진별 영화 개수:")
    print(actors_counts)

    return directors_counts, actors_counts


def recommend_movies_by_popular_actors(df, actors_counts):
    """
    인기 배우 기준으로 영화 추천
    """
    popular_actors = actors_counts[actors_counts > 1].index
    recommended_movies = df[df['출연진_리스트'].apply(lambda x: any(actor in x for actor in popular_actors))]
    print("\n인기 배우가 출연한 영화:")
    print(recommended_movies[['제목', '출연진']])
    return recommended_movies


def recommend_movies_by_genre(df, genre, top_n=3):
    """
    특정 장르 기준으로 영화 추천
    """
    genre_counts = df['장르'].value_counts()
    print("\n장르별 영화 개수 :")
    print(genre_counts)

    recommend_movies = df[df['장르'] == genre]
    print(f"\n'{genre}' 장르의 영화:")
    print(recommend_movies[['제목', '출연진']])

    print(f"\n'{genre}' 장르 상위 {top_n} 추천 영화:")
    print(recommend_movies.head(top_n)[['제목', '감독']])
    return recommend_movies.head(top_n)



def main():
    file_path = "prob-0101.csv"

    df = pd.read_csv(file_path)

    # 기본 분석
    basic_analysis(df)

    # 통계 계산
    count_statistics(df)

    # 중복 조건 분석
    directors_counts, actors_counts = analyze_duplicates(df)

    # 인기 배우 기준 영화 추천
    recommend_movies_by_popular_actors(df, actors_counts)

    # 특정 장르 기준 영화 추천
    genre = "액션"
    recommend_movies_by_genre(df, genre)

if __name__ == "__main__":
    main()