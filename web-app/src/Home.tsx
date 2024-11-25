import eleven from './assets/11.gif'

export default function Home() {
  return (
    <div className="text-center">
      <h2 className="text-xl p-2">Home</h2>
      <h3 className="text-l p-2">Welcome to 11x Genomics</h3>
      <p>Marty DiBerg (as played by Rob Reiner): Why don't you just make ten <s>louder</s> better and make ten be the top <s>genomics</s> and make that a little <s>louder</s> better? </p>
      <p>Me:</p>
      <img src={eleven} className="mx-auto" alt="These go to eleven." />
    </div>
  );
}
