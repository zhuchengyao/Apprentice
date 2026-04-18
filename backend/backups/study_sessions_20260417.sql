--
-- PostgreSQL database dump
--

\restrict oDTVnUPbhBCHc9U1h2x23BTCU7R6JOlVJe6LVAj1YH8k6LAjytZXj1roLt61vBd

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg12+1)
-- Dumped by pg_dump version 16.12 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: study_sessions; Type: TABLE; Schema: public; Owner: apprentice
--

CREATE TABLE public.study_sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    book_id uuid NOT NULL,
    section_id uuid NOT NULL,
    started_at timestamp without time zone NOT NULL,
    ended_at timestamp without time zone,
    interactions json,
    mastery_before double precision NOT NULL,
    mastery_after double precision
);


ALTER TABLE public.study_sessions OWNER TO apprentice;

--
-- Data for Name: study_sessions; Type: TABLE DATA; Schema: public; Owner: apprentice
--



--
-- Name: study_sessions study_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: apprentice
--

ALTER TABLE ONLY public.study_sessions
    ADD CONSTRAINT study_sessions_pkey PRIMARY KEY (id);


--
-- Name: study_sessions study_sessions_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apprentice
--

ALTER TABLE ONLY public.study_sessions
    ADD CONSTRAINT study_sessions_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(id) ON DELETE CASCADE;


--
-- Name: study_sessions study_sessions_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apprentice
--

ALTER TABLE ONLY public.study_sessions
    ADD CONSTRAINT study_sessions_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.sections(id) ON DELETE CASCADE;


--
-- Name: study_sessions study_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: apprentice
--

ALTER TABLE ONLY public.study_sessions
    ADD CONSTRAINT study_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict oDTVnUPbhBCHc9U1h2x23BTCU7R6JOlVJe6LVAj1YH8k6LAjytZXj1roLt61vBd

