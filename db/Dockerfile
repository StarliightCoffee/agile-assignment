FROM postgres:18

EXPOSE 5432

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=CoolPass321
ENV POSTGRES_DB=gym_pro

COPY init/ /docker-entrypoint-initdb.d/