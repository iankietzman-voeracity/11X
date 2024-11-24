import ky from "ky";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState({});

  useEffect(() => {
    console.log("updating data");

    async function fetchData() {
      const response = await ky.get("http://localhost:8000/");
      console.log(response);
      // console.log(await response.json());
      setData(await response.json());
    }

    fetchData();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {JSON.stringify(data)}
    </div>
  );
}
