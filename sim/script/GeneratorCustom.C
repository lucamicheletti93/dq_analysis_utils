AliGenerator *GeneratorCustom(TString opt = "")

{
  printf("Utilizzo PYTHIA8\n");
  AliGenPythiaPlus* pyth = (AliGenPythiaPlus*)GeneratorPythia8(kPythia8Tune_Monash2013);
  printf("GeneratorCustom MB \n");

   pyth->SetCutOnChild(1);
   pyth->SetPdgCodeParticleforAcceptanceCut(13);
   pyth->SetChildYRange(-4.1, -2.4);
   pyth->SetChildPtRange(0, 10000.);

  return pyth;

}
