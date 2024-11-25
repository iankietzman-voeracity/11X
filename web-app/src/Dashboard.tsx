import ky from "ky";
import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function Dashboard() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const response = await ky.get("http://localhost:8000/");
      setData(await response.json());
      setLoading(false);
    }
    fetchData();
  }, []);

  useEffect(() => {
    console.log(data);
  }, [data]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2 className="text-xl p-2">Dashboard</h2>
      <h2 className="text-l p-2">Cell Matrix</h2>
      <Table>
        <TableCaption>
          Raw data can be seen in the console for your convenience.
        </TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>Cell</TableHead>
            {data.refGen.map((gene, index) => (
              <TableHead key={index}>{gene.gene}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.count_matrix.cells.map((barcode, index) => (
            <TableRow key={index} role="row">
              <TableCell>{barcode}</TableCell>
              {data.refGen.map((gene, gene_index) => (
                <TableCell key={gene_index}>
                  {data.count_matrix.data[barcode].genes[gene.gene]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
