FROM postgres:15

ENV POSTGRES_DB=shelter
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password

# Expose the PostgreSQL port
EXPOSE 5432
