DROP TABLE users;
DROP TABLE posts;

CREATE TABLE IF NOT EXISTS users (
    id integer NOT NULL,
    facebook_id character varying,
    user_name character varying,
    user_pic character varying,
    access_token character varying,
    banned boolean DEFAULT false
);

CREATE SEQUENCE IF NOT EXISTS users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_id_seq OWNED BY users.id;
ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

CREATE TABLE IF NOT EXISTS posts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_name character varying,
    post_time timestamp without time zone,
    post_body character varying,
    is_bullying boolean DEFAULT false,
    bullying_words character varying[] DEFAULT array[]::varchar[]
);

CREATE SEQUENCE IF NOT EXISTS posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;
ALTER TABLE ONLY posts ALTER COLUMN id SET DEFAULT nextval('posts_id_seq'::regclass);
