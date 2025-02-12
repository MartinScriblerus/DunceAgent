// "use client";

import { ChatWindow } from "@/components/ChatWindow";
import ShowVectorDbs from "@/components/ShowVectorDbs";
import "../app/globals.css"

import useCustomInput from "@/hooks/useCustomInput";
import { FormEventHandler, useEffect, useState, useContext } from "react";

import HomeClient from "./home_client/ClientHome";

export default async function Home() {
  return (
    <HomeClient />
  );
}


