import { ReactNode } from "react";

export default function RootLayout(props: { children: ReactNode }) {
  return <>
      <nav>{props.children}</nav></>;
}